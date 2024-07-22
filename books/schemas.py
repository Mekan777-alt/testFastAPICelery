from typing import Optional, List
from genres.schemas import GenreResponseSchema, GenreOptionalCreateSchema

from pydantic import BaseModel, Field


class BookResponseSchema(BaseModel):
    id: int = Field(..., example=5)
    title: str = Field(..., example='Book')
    price: float = Field(..., example=100)
    pages: int = Field(..., example=100)
    author_id: int = Field(..., example=5)
    genres: List[GenreResponseSchema] = []

    class Config:
        from_attributes = True


class BooksSchema(BaseModel):
    title: str = Field(..., example='Book')
    price: float = Field(..., example=100)
    pages: int = Field(..., example=100)
    author_id: int = Field(..., example=5)
    genres: List[GenreResponseSchema] = []


class BookPartialUpdate(BaseModel):
    title: Optional[str] = Field(None, example='Book')
    price: Optional[float] = Field(None, example=100)
    pages: Optional[int] = Field(None, example=100)
    author_id: Optional[int] = Field(None, example=5)
    genres: Optional[List[GenreOptionalCreateSchema]] = Field(None, example=[])
