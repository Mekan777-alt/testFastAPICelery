from sqlalchemy.ext.asyncio import AsyncSession

from genres.models import Genre
from genres.schemas import GenreCreateUpdateSchema
from genres.repositories import GenreRepository


class GenreService:

    def __init__(self, db: AsyncSession):
        self.db = db
        self.genre_repository = GenreRepository(db)

    async def get_all_genres(self):
        return await self.genre_repository.get_all_genres()

    async def create_new_genre(self, genre: GenreCreateUpdateSchema):
        new_genre = Genre(name=genre.name)
        return await self.genre_repository.create_genre(new_genre)

    async def get_genre(self, genre_id: int):
        return await self.genre_repository.get_genre(genre_id)

    async def update_genre(self, genre_id: int, genre: GenreCreateUpdateSchema):
        return await self.genre_repository.update_genre(genre_id, genre)

    async def delete_genre(self, genre_id: int):
        return await self.genre_repository.delete_genre(genre_id)
