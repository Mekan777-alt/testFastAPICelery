from pydantic import BaseModel, Field


class GenreResponseSchema(BaseModel):
    id: int = Field(..., example=1)
    name: str = Field(..., example="Fiction")

    class Config:
        from_attributes = True


class GenreCreateUpdateSchema(BaseModel):
    name: str = Field(..., example="Fiction")


