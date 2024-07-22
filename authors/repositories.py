from sqlalchemy.ext.asyncio import AsyncSession
from authors.models import Authors
from sqlalchemy.future import select


class AuthorRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_authors(self):
        result = await self.db.execute(select(Authors))
        return result.scalars().all()

    async def get_author(self, author_id):
        result = await self.db.execute(select(Authors).where(Authors.id == author_id))
        return result.scalar()

    async def create_author(self, author: Authors):
        self.db.add(author)

        await self.db.commit()
        await self.db.refresh(author)

        return author

    async def update_author(self, author: Authors):
        await self.db.commit()
        await self.db.refresh(author)

        return author

    async def delete_author(self, author):
        await self.db.delete(author)
        await self.db.commit()
