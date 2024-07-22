from books.repositories import BookRepository
from sqlalchemy.ext.asyncio import AsyncSession
from books.models import Book, BookGenreAssociation
from books.schemas import BooksSchema, BookResponseSchema


class BooksService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.book_repository = BookRepository(db)

    async def get_all_books(self):
        return await self.book_repository.get_all_books()

    async def get_book(self, book_id: int):
        result = await self.book_repository.get_book(book_id)
        return result

    async def create_book(self, book: BooksSchema):
        new_book = Book(
            title=book.title,
            price=book.price,
            pages=book.pages,
            author_id=book.author_id,
        )
        return await self.book_repository.create_book(new_book)
