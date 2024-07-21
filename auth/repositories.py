from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from auth.models import Auth


class AuthRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_by_email(self, email: str):
        result = await self.db.execute(select(Auth).where(Auth.email == email))
        return result.scalar()

    async def create_user(self, user):
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user
