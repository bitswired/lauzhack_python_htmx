import base64
import io
from pathlib import Path
from typing import Annotated

import faker
import httpx
from litestar import Controller, Litestar, Router, get, post
from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.enums import RequestEncodingType
from litestar.exceptions import HTTPException
from litestar.params import Body
from litestar.response import Template
from litestar.static_files.config import StaticFilesConfig
from litestar.template.config import TemplateConfig
from PIL import Image
from pydantic import BaseModel, Field
from pydantic.networks import Url


class LiveDataController(Controller):
    path = "/"

    @get()
    async def index_view(self) -> Template:
        return Template(
            template_name="live-data/index.html",
        )

    @get("/data")
    async def get_live_data(self) -> Template:
        # generate fake stock data
        fake = faker.Faker()
        data = {
            "name": fake.company(),
            "price": fake.pyfloat(left_digits=4, right_digits=2, positive=True),
            "change": fake.pyfloat(left_digits=2, right_digits=2, positive=True),
        }

        return Template(
            template_name="live-data/data-update.html",
            context={
                "data": data,
            },
        )


live_data_router = Router(path="/live-data", route_handlers=[LiveDataController])


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


form_submission_controller = Router(
    path="/form-submission", route_handlers=[FormSubmissionController]
)

# Random data for filtering and sorting
faker = faker.Faker()
data_filtering_sorting = [
    {
        "name": faker.name(),
        "age": faker.pyint(min_value=18, max_value=100),
        "email": faker.email(),
        "city": faker.city(),
        "country": faker.country(),
        "phone": faker.phone_number(),
    }
    for _ in range(100)
]


class FilteringSortingController(Controller):
    path = "/"

    @get()
    async def index_view(self) -> Template:
        return Template(
            template_name="filtering-sorting/index.html",
            context={
                "clients": data_filtering_sorting,
            },
        )

    @get("/process")
    async def process(
        self,
        sort: str,
        filter: str,
    ) -> Template:
        print(filter, sort)

        if filter:
            data = [
                client
                for client in data_filtering_sorting
                if filter.lower() in client["name"].lower()
            ]
        else:
            data = data_filtering_sorting

        if sort != "none":
            data = sorted(data, key=lambda x: x[sort])

        return Template(
            template_name="filtering-sorting/content.html",
            context={
                "clients": data,
            },
        )


@get()
async def index_view() -> Template:
    return Template(
        template_name="index.html",
    )


filtering_sorting_router = Router(
    path="/filtering-sorting", route_handlers=[FilteringSortingController]
)


app = Litestar(
    route_handlers=[
        index_view,
        live_data_router,
        form_submission_controller,
        filtering_sorting_router,
    ],
    static_files_config=[
        StaticFilesConfig(directories=[Path("static")], path="/static"),
    ],
    template_config=TemplateConfig(
        directory=Path(__file__).parent / "templates",
        engine=JinjaTemplateEngine,
    ),
)
