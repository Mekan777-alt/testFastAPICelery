from typing import Optional

from pydantic import BaseModel, Field


class AuthorResponseSchemas(BaseModel):
    id: int = Field(..., example="1")
    first_name: str = Field(..., example="<NAME>")
    last_name: str = Field(..., example="<LAST NAME>")
    avatar: Optional[str] = Field(..., example="https://avatars1.githubusercontent.com")
