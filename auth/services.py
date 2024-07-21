from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, Depends
from jose import jwt, JWTError
from datetime import datetime, timedelta
from auth.repositories import AuthRepository
from auth.schemas import TokenData, UserCreate
from auth.models import Auth
from core.config import settings
from core.security import verify_password, get_password_hash, create_access_token


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.auth_repository = AuthRepository(db)

    async def authenticate_user(self, email: str, password: str):
        user = await self.auth_repository.get_user_by_email(email)

        if not user:
            return False

        if not verify_password(password, user.hashed_password):
            return False

        return user

    async def create_access_token_service(self, user: Auth):
        token_data = {"sub": user.email}
        return create_access_token(token_data)

    async def create_user(self, user: UserCreate):
        hashed_password = get_password_hash(user.password)
        db_user = Auth(
            email=user.email,
            hashed_password=hashed_password
        )
        return await self.auth_repository.create_user(db_user)

