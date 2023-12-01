from typing import Annotated, Optional

from litestar import Controller, Request, Router, get, post
from litestar.datastructures import Cookie, State
from litestar.enums import RequestEncodingType
from litestar.exceptions import HTTPException
from litestar.params import Body
from litestar.response import Redirect, Template
from litestar.status_codes import HTTP_401_UNAUTHORIZED
from openai import AsyncClient

from .db.models import User
from .dtos import CreateUserDto, GenerateImageDto
from .state import AppState

openai_client = AsyncClient()


class MainController(Controller):
    path = "/"

    @get()
    async def index_view(
        self,
        request: Request[Optional[User], str, State],
    ) -> Template:
        return Template(template_name="base.html", context={"user": request.user})

    @get("/logout")
    async def logout(
        self,
    ) -> Redirect:
        x = Redirect("/")
        x.delete_cookie("pictorial-session")
        return x

    @get("/login")
    async def login_view(
        self,
        request: Request[Optional[User], str, State],
    ) -> Template:
        return Template(template_name="login.html", context={"user": request.user})

    @post("/login")
    async def login(
        self,
        data: Annotated[
            CreateUserDto, Body(media_type=RequestEncodingType.URL_ENCODED)
        ],
        state: AppState,
    ) -> Redirect:
        user = await state.repository.get_user_by_credentials(data.email, data.password)
        if not user:
            raise HTTPException(
                detail="Invalid Credentials", status_code=HTTP_401_UNAUTHORIZED
            )

        x = Redirect("/")
        x.cookies.append(Cookie(key="pictorial-session", value=user.id, httponly=True))
        return x

    @get("/signup")
    async def signup_view(
        self,
        request: Request[Optional[User], str, State],
    ) -> Template:
        return Template(template_name="signup.html", context={"user": request.user})

    @post("/signup")
    async def create_user(
        self,
        data: Annotated[
            CreateUserDto, Body(media_type=RequestEncodingType.URL_ENCODED)
        ],
        state: AppState,
    ) -> Redirect:
        user_id = await state.repository.create_user(data.email, data.password)
        print(user_id)
        return Redirect("/login")


main_router = Router(path="/", route_handlers=[MainController])


import base64
from pathlib import Path
from uuid import uuid4

import aiofiles


async def save_image(b64_string: str) -> (str, str):
    # Decode the base64 string
    image_data = base64.b64decode(b64_string)

    name = str(uuid4())
    path = Path("static") / f"{name}.png"
    # Open the file in async mode and save the content
    async with aiofiles.open(path, "wb") as f:
        await f.write(image_data)

    return name, str(path)


class GenerateController(Controller):
    path = "/"

    @get()
    async def index_view(
        self,
        request: Request[Optional[User], str, State],
    ) -> Template:
        return Template(
            template_name="generate/index.html", context={"user": request.user}
        )

    @post("image")
    async def generate_image(
        self,
        request: Request[Optional[User], str, State],
        data: Annotated[
            GenerateImageDto, Body(media_type=RequestEncodingType.URL_ENCODED)
        ],
        state: AppState,
    ) -> None:
        print(data)

        res = await openai_client.images.generate(
            model="dall-e-3",
            prompt=data.prompt,
            n=1,
            size="1024x1024",
            response_format="b64_json",
        )

        # Save image
        b64_string = res.data[0].b64_json
        img_id, img_path = await save_image(b64_string)

        # Add to database
        await state.repository.create_generation(request.user.id, img_id, data.prompt)

        return Template(
            template_name="generate/generate-image-output.html",
            context={"prompt": data.prompt, "url": f"/{img_path}"},
        )


generate_router = Router(path="/generate", route_handlers=[GenerateController])


class LibraryRouter(Controller):
    path = "/"

    @get()
    async def index_view(
        self, request: Request[Optional[User], str, State], state: AppState
    ) -> Template:
        generations = await state.repository.get_user_generations(request.user.id)
        print(generations)

        return Template(
            template_name="library/index.html",
            context={"user": request.user, "generations": generations},
        )


library_router = Router(path="/library", route_handlers=[LibraryRouter])
