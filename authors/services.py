import os
from uuid import uuid4

from fastapi import HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from authors.models import Authors
from authors.repositories import AuthorRepository
from starlette import status


class AuthorService:

    def __init__(self, db: AsyncSession):
        self.db = db
        self.author_repository = AuthorRepository(db)

    async def get_all_authors(self):
        return await self.author_repository.get_authors()

    async def get_author(self, author_id):
        author = await self.author_repository.get_author(author_id)

        if not author:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")

        return author

    async def create_author(self, first_name: str, last_name: str, avatar: UploadFile):
        new_author = Authors(
            first_name=first_name,
            last_name=last_name,
            avatar=await self._save_photo(avatar)
        )

        return await self.author_repository.create_author(new_author)

    async def update_author(self, author_id, first_name: str, last_name: str, avatar: UploadFile):
        existing_author = await self.author_repository.get_author(author_id)

        if not existing_author:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")

        if existing_author.avatar:
            await self._delete_photo(author_id)

        avatar_path = await self._save_photo(avatar)

        existing_author.first_name = first_name
        existing_author.last_name = last_name
        existing_author.avatar = avatar_path

        await self.author_repository.update_author(existing_author)
        return existing_author

    async def partial_update_author(self, author_id, first_name: str, last_name: str, avatar: UploadFile):
        existing_author = await self.author_repository.get_author(author_id)

        if not existing_author:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")

        if existing_author.avatar:
            await self._delete_photo(author_id)

        if avatar is not None:
            avatar_path = await self._save_photo(avatar)
            existing_author.avatar = avatar_path

        if first_name is not None:
            existing_author.first_name = first_name
        if last_name is not None:
            existing_author.last_name = last_name

        await self.author_repository.update_author(existing_author)
        return existing_author

    async def delete_author(self, author_id):
        author = await self.author_repository.get_author(author_id)

        if not author:

            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")

        if author.avatar:
            await self._delete_photo(author_id)

        await self.author_repository.delete_author(author)

    async def _save_photo(self, avatar: UploadFile):
        if avatar:

            avatar_directory = "static/avatars"
            os.makedirs(avatar_directory, exist_ok=True)

            avatar_filename = f"{uuid4()}.jpg"
            avatar_path = f"static/avatars/{avatar_filename}"

            with open(avatar_path, "wb") as buffer:
                buffer.write(await avatar.read())

            return avatar_path

        else:
            return None

    async def _delete_photo(self, author_id: int):
        author = await self.author_repository.get_author(author_id)

        if not author:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")

        if author.avatar:

            if os.path.exists(author.avatar):
                os.remove(author.avatar)

            author.avatar = None
            await self.author_repository.update_author(author)
