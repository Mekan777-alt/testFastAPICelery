from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from auth.models import Auth


class AuthRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_by_email(self, email: str):
        result = await self.db.execute(select(Auth).where(Auth.email == email))
        return result.scalar()
