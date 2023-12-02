import base64
import io
from typing import Annotated

import httpx
from litestar import Controller, Router, get, post
from litestar.enums import RequestEncodingType
from litestar.exceptions import HTTPException
from litestar.params import Body
from litestar.response import Template
from PIL import Image
from pydantic import BaseModel, Field
from pydantic.networks import Url


class ResizeImageDto(BaseModel):
    url: Url
    size: Annotated[int, Field(gt=0, le=200)]


async def validate_image_url(url: str) -> bool:
    try:
        async with httpx.AsyncClient() as client:
            r = await client.get(url)
    except httpx.UnsupportedProtocol:
        return False

    content_type = r.headers.get("content-type")

    if content_type and content_type.startswith("image/"):
        return True
    else:
        return False


class FormSubmissionController(Controller):
    path = "/"

    @get()
    async def index_view(self) -> Template:
        return Template(
            template_name="form-submission/index.html",
        )

    @get("/preview/size")
    async def preview_size(self, size: int) -> int:
        return Template(
            template_name="form-submission/size-preview.html",
            context={
                "size": size,
            },
        )

    @get("/preview/image")
    async def preview_image(self, url: str) -> int:
        is_valid = await validate_image_url(url)

        if is_valid:
            return Template(
                template_name="form-submission/image-preview.html",
                context={
                    "url": url,
                },
            )
        else:
            return Template(
                template_name="form-submission/image-preview.html",
                context={"error": True},
            )

    @post("/resize")
    async def resize(
        self,
        data: Annotated[
            ResizeImageDto, Body(media_type=RequestEncodingType.URL_ENCODED)
        ],
    ) -> Template:
        is_valid = await validate_image_url(str(data.url))

        if not is_valid:
            raise HTTPException(
                detail="Invalid image URL", status_code=httpx.HTTPStatus.BAD_REQUEST
            )

        # Use httpx to download the image
        async with httpx.AsyncClient() as client:
            r = await client.get(str(data.url))

        content_type = r.headers.get("content-type")

        # Open the image with PIL
        image = Image.open(io.BytesIO(r.content))

        # Calculate the new size
        new_size = tuple(map(lambda x: int(x * data.size / 100), image.size))

        # Resize the image
        resized_image = image.resize(new_size)

        # Convert to base64
        buffered = io.BytesIO()
        resized_image.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode()

        # Transform to data URL, respect content type
        data_url = f"data:{content_type};base64,{img_str}"

        return Template(
            template_name="form-submission/resize-output.html",
            context={
                "url": data_url,
            },
        )


form_submission_router = Router(
    path="/form-submission", route_handlers=[FormSubmissionController]
)
