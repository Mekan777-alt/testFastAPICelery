from pydantic import BaseModel
from typing import Optional


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str
    first_name: str
    last_name: str


class UserInDB(UserBase):
    hashed_password: str


class User(UserBase):
    id: int
    first_name: str
    last_name: str

    class Config:
        orm_mode = True
