from fastapi import APIRouter, Depends
from starlette import status
from books.schemas import BookSchema
from books.services import BooksService

from db.session import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

router = APIRouter()


@router.get("/books", summary="Возвращает все книги", status_code=status.HTTP_200_OK,
            response_model=List[BookSchema])
async def get_all_books(session: AsyncSession = Depends(get_session)):
    """
    Возвращает все книги
    """
    service = BooksService(session)
    books = await service.get_all_books()

    return books


@router.get("/books/{book_id}", summary="Возвращает книгу по ID", status_code=status.HTTP_200_OK,
            response_model=BookSchema)
async def get_book_by_id(book_id: int, session: AsyncSession = Depends(get_session)):
    """
    Возвращает книгу по ID\n
    param book_id: Принимаеи int значение
    """
    service = BooksService(session)
    book = await service.get_book(book_id)

    return book





