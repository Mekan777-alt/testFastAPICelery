from sqlalchemy.ext.asyncio import AsyncSession
from books.models import BookGenreAssociation


class BookAssociationRepositories:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_book_association(self, association):
        self.db.add(association)

        await self.db.commit()
        await self.db.refresh(association)

        return association
