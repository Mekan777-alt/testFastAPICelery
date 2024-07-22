from fastapi import APIRouter, Depends
from starlette import status
from books.schemas import BookResponseSchema, BooksSchema
from books.services import BooksService, BookAssociationService

from db.session import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

router = APIRouter()


@router.get("/books", summary="Возвращает все книги", status_code=status.HTTP_200_OK,
            response_model=List[BookResponseSchema])
async def get_all_books(session: AsyncSession = Depends(get_session)):
    """
    Возвращает все книги
    """
    service = BooksService(session)
    books = await service.get_all_books()

    return books


@router.get("/books/{book_id}", summary="Возвращает книгу по ID", status_code=status.HTTP_200_OK,
            response_model=BookResponseSchema)
async def get_book_by_id(book_id: int, session: AsyncSession = Depends(get_session)):
    """
    Возвращает книгу по ID\n
    param book_id: Принимаеи int значение
    """
    service = BooksService(session)
    book = await service.get_book(book_id)

    return book


@router.post('/books', summary="Добавление книги", status_code=status.HTTP_201_CREATED,
             response_model=BooksSchema)
async def create_book(book: BooksSchema, session: AsyncSession = Depends(get_session)):
    """

    :param book: Принимает схему создание книги
    :return: Возвращает созданный экзмепляр книги
    """

    books_service = BooksService(session)
    books_association_service = BookAssociationService(session)

    created_book = await books_service.create_book(book)

    if created_book:

        await books_association_service.create_book_association(
            book_id=created_book.id, genre_id=book.genre_id)

    return created_book


@router.put('/books/{book_id}', summary="Полное обновление книги по ID", status_code=status.HTTP_200_OK)
async def all_update_books(book_id: int, session: AsyncSession = Depends(get_session)):
    pass
