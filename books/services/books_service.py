from fastapi import HTTPException
from starlette import status

from books.repositories import BookRepository
from sqlalchemy.ext.asyncio import AsyncSession
from books.models import Book
from books.schemas import BooksSchema, BookResponseSchema, BookPartialUpdate
from books.services.book_association_service import BookAssociationService
from genres.schemas import GenreResponseSchema
from authors.repositories import AuthorRepository


class BooksService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.book_repository = BookRepository(db)
        self.book_association_service = BookAssociationService(db)
        self.author_repository = AuthorRepository(db)

    async def get_all_books(self):
        books = await self.book_repository.get_all_books()
        return [self._convert_to_response_schema(book) for book in books]

    async def get_book(self, book_id: int):
        book = await self.book_repository.get_book(book_id)

        if not book:
            raise HTTPException(status_code=404, detail="Book not found")

        return self._convert_to_response_schema(book)

    async def create_book(self, book: BooksSchema):
        author = await self.author_repository.get_author(book.author_id)

        if not author:
            raise HTTPException(status_code=404, detail="Author not found or add the author")

        new_book = Book(
            title=book.title,
            price=book.price,
            pages=book.pages,
            author_id=book.author_id,
        )

        created_book = await self.book_repository.create_book(new_book)

        for genre in book.genres:

            if genre.id:
                await self.book_association_service.create_book_association(created_book.id, genre.id)

        return created_book

    async def update_book(self, book_id: int, book: BooksSchema):
        existing_book = await self.book_repository.get_book(book_id)

        if not existing_book:
            raise HTTPException(status_code=404, detail="Book not found")

        existing_book.title = book.title
        existing_book.price = book.price
        existing_book.pages = book.pages
        existing_book.author_id = book.author_id

        await self.book_association_service.delete_book_association(book_id)

        for genre in book.genres:

            if genre.id:
                await self.book_association_service.create_book_association(existing_book.id, genre.id)

        await self.book_repository.update_book(existing_book)
        return self._convert_to_response_schema(existing_book)

    async def partial_update_book(self, book_id: int, book: BookPartialUpdate):
        existing_book = await self.book_repository.get_book(book_id)

        if not existing_book:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

        if book.title is not None:
            existing_book.title = book.title
        if book.price is not None:
            existing_book.price = book.price
        if book.pages is not None:
            existing_book.pages = book.pages
        if book.author_id is not None:
            existing_book.author_id = book.author_id

        if book.genres is not None:
            await self.book_association_service.delete_book_association(book_id)

            for genre in book.genres:
                if genre.id:
                    await self.book_association_service.create_book_association(existing_book.id, genre.id)

        await self.book_repository.update_book(existing_book)
        return self._convert_to_response_schema(existing_book)

    async def delete_book(self, book_id: int):
        book = await self.book_repository.get_book(book_id)

        if not book:

            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

        return await self.book_repository.delete_book(book)

    def _convert_to_response_schema(self, book: Book) -> BookResponseSchema:
        genres = [GenreResponseSchema(id=assoc.genre.id, name=assoc.genre.name) for assoc in book.books_assoc]
        return BookResponseSchema(
            id=book.id,
            title=book.title,
            price=book.price,
            pages=book.pages,
            author_id=book.author_id,
            genres=genres
        )
