from sqlalchemy.ext.asyncio import AsyncSession
from books.repositories import BookAssociationRepositories
from books.models import BookGenreAssociation


class BookAssociationService:
    def __init__(self, db):
        self.db = db
        self.book_association_repository = BookAssociationRepositories(db)

    async def create_book_association(self, book_id: int, genre_id: int):
        new_association = BookGenreAssociation(book_id=book_id, genre_id=genre_id)
        return await self.book_association_repository.create_book_association(new_association)