from pydantic import BaseModel
from datetime import date


class BookingCreate(BaseModel):
    start_date: date
    end_date: date


class BookingResponse(BaseModel):
    id: int
    book_id: int
    start_date: date
    end_date: date
    status: str
