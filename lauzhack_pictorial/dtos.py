from pydantic import BaseModel


class CreateUserDto(BaseModel):
    email: str
    password: str


class GenerateImageDto(BaseModel):
    prompt: str
