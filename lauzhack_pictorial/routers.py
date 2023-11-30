from typing import Annotated, Optional

from litestar import Controller, Request, Router, get, post
from litestar.datastructures import Cookie, State
from litestar.enums import RequestEncodingType
from litestar.exceptions import HTTPException
from litestar.params import Body
from litestar.response import Redirect, Template
from litestar.status_codes import HTTP_401_UNAUTHORIZED

from .db.models import User
from .dtos import CreateUserDto
from .state import AppState


class MainController(Controller):
    path = "/"

    @get()
    async def home_view(
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
