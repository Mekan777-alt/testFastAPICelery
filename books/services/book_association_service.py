from sqlalchemy.ext.asyncio import AsyncSession
from books.repositories import BookAssociationRepositories
from books.models import BookGenreAssociation
from sqlalchemy.future import select


class BookAssociationService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.book_association_repository = BookAssociationRepositories(db)

    async def create_book_association(self, book_id: int, genre_id: int):
        new_association = BookGenreAssociation(book_id=book_id, genre_id=genre_id)
        return await self.book_association_repository.create_book_association(new_association)

    async def delete_book_association(self, book_id: int):
        existing_associations = await self.db.execute(
            select(BookGenreAssociation).where(BookGenreAssociation.book_id == book_id)
        )
        for association in existing_associations.scalars().all():
            await self.db.delete(association)
        await self.db.commit()
