from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from genres.models import Genre


class GenreRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_genres(self):
        result = await self.db.execute(select(Genre))
        return result.scalars().all()

    async def create_genre(self, genre):
        self.db.add(genre)

        await self.db.commit()
        await self.db.refresh(genre)

        return genre

    async def get_genre(self, genre_id):
        genre = await self.db.execute(select(Genre).where(Genre.id == genre_id))
        genre = genre.scalar()

        if genre is None:

            raise HTTPException(status_code=404, detail="Genre not found")

        return genre

    async def update_genre(self, genre_id, genre):
        genre_db = await self.db.execute(select(Genre).where(Genre.id == genre_id))
        genre_db = genre_db.scalar()

        if genre_db is None:

            raise HTTPException(status_code=404, detail="Genre not found")

        genre_db.name = genre.name

        await self.db.commit()
        await self.db.refresh(genre_db)

        return genre_db

    async def delete_genre(self, genre_id):
        genre = await self.db.execute(select(Genre).where(Genre.id == genre_id))
        genre = genre.scalar()

        if genre is None:
            raise HTTPException(status_code=404, detail="Genre not found")

        await self.db.delete(genre)
        await self.db.commit()
