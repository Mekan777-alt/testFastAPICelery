from typing import List

from books.repositories import BookRepository
from sqlalchemy.ext.asyncio import AsyncSession

from books.schemas import BookSchema


class BooksService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.book_repository = BookRepository(db)

    async def get_all_books(self):
        return await self.book_repository.get_all_books()

    async def get_book(self, book_id: int):
        result = await self.book_repository.get_book(book_id)
        return result
