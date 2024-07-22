from pydantic import BaseModel, Field
from datetime import datetime


class BookingCreate(BaseModel):
    start_datetime: datetime = Field(..., example="2024-07-22 18:02:59")
    end_datetime: datetime = Field(..., example="2024-07-22 20:02:59")


class BookingResponse(BaseModel):
    id: int
    book_id: int
    start_date: datetime
    end_date: datetime
    status: str
