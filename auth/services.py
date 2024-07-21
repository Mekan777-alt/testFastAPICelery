from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, Depends
from jose import jwt, JWTError
from datetime import datetime, timedelta
from passlib.context import CryptContext
from auth.repositories import AuthRepository
from auth.schemas import TokenData
from auth.models import Auth
from core.config import settings
from core.security import verify_password, get_password_hash, create_access_token


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.auth_repository = AuthRepository(db)

    async def authenticate_user(self, email: str, password: str):
        user = self.auth_repository.get_user_by_email(email)

        if not user:
            return False

        if not verify_password(password, user.hashed_password):
            return False

        return user

    async def create_access_token(self, user: Auth):
        token_data = {"sub": user.email}
        return create_access_token(token_data)

