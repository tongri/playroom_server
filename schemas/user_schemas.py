from pydantic import BaseModel, Field


class User(BaseModel):
    username: str


class UserIn(User):
    password: str


class UserOut(User):
    id: int
    is_staff: bool = Field(default=False)


class UserPublic(User):
    id: int


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
    is_staff: bool = False
