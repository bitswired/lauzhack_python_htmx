from pydantic import BaseModel


class User(BaseModel):
    id: int
    email: str
    password: str


class Generation(BaseModel):
    id: int
    user_id: int
    image_id: str
    prompt: str
