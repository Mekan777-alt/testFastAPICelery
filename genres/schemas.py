from typing import Optional

from pydantic import BaseModel, Field


class GenreResponseSchema(BaseModel):
    id: int = Field(..., example=1)
    name: str = Field(..., example="Fiction")

    class Config:
        from_attributes = True


class GenreCreateUpdateSchema(BaseModel):
    name: str = Field(..., example="Fiction")


class GenreOptionalCreateSchema(BaseModel):
    id: Optional[int] = Field(..., example=1)
    name: Optional[str] = Field(..., example="Fiction")
