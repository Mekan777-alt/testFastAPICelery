from pydantic import BaseModel, Field


class BookSchema(BaseModel):
    id: int = Field(..., example=5)
    title: str = Field(..., example='Book')
    price: float = Field(..., example=100)
    pages: int = Field(..., example=100)
    author_id: int = Field(..., example=5)
