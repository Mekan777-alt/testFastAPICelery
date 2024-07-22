from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from books.models import Book, BookGenreAssociation
from sqlalchemy.future import select


class BookRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_books(self):
        result = await self.db.execute(
            select(Book).options(selectinload(Book.books_assoc).selectinload(BookGenreAssociation.genre))
        )
        books = result.scalars().all()
        return books

    async def get_book(self, book_id):
        result = await self.db.execute(
            select(Book).where(Book.id == book_id).options(
                selectinload(Book.books_assoc).selectinload(BookGenreAssociation.genre)
            )
        )
        return result.scalar()

    async def create_book(self, book):
        self.db.add(book)
        await self.db.commit()
        await self.db.refresh(book)

        return book

    async def update_book(self, existing_book):
        await self.db.commit()
        await self.db.refresh(existing_book)

        return existing_book
