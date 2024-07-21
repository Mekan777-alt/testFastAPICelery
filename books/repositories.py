from sqlalchemy.ext.asyncio import AsyncSession
from books.models import Book
from sqlalchemy.future import select


class BookRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_books(self):
        result = await self.db.execute(select(Book))
        return result.scalars().all()

    async def get_book(self, book_id):
        result = await self.db.execute(select(Book).where(Book.id == book_id))
        return result.scalar()
