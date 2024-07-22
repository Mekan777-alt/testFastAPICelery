from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from books.models import Book, BookGenreAssociation
from sqlalchemy.future import select

from books.schemas import BookResponseSchema
from genres.schemas import GenreResponseSchema


class BookRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_books(self):
        result = await self.db.execute(
            select(Book).options(selectinload(Book.books_assoc).selectinload(BookGenreAssociation.genre))
        )
        books = result.scalars().all()
        book_responses = []
        for book in books:
            genres = [assoc.genre for assoc in book.books_assoc]
            genre_schemas = [GenreResponseSchema(id=genre.id, name=genre.name) for genre in genres]
            book_response = BookResponseSchema(
                id=book.id,
                title=book.title,
                price=book.price,
                pages=book.pages,
                author_id=book.author_id,
                genres=genre_schemas
            )
            book_responses.append(book_response)
        return book_responses

    async def get_book(self, book_id):
        result = await self.db.execute(
            select(Book).where(Book.id == book_id).options(
                selectinload(Book.books_assoc).selectinload(BookGenreAssociation.genre)
            )
        )
        book = result.scalar()
        genres = [assoc.genre for assoc in book.books_assoc]
        genres_schemas = [GenreResponseSchema(id=genre.id, name=genre.name) for genre in genres]
        book_response = BookResponseSchema(
            id=book.id,
            title=book.title,
            price=book.price,
            pages=book.pages,
            author_id=book.author_id,
            genres=genres_schemas
        )
        return book_response

    async def create_book(self, book):
        self.db.add(book)
        await self.db.commit()
        await self.db.refresh(book)
        return book
