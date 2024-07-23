from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from auth.repositories import AuthRepository
from auth.schemas import UserCreate
from auth.models import Auth
from starlette import status
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
        email = self.auth_repository.get_user_by_email(user.email)

        if email:
            raise HTTPException(
                status_code=status.HTTP_200_OK,
                detail="Email already registered",
            )
        hashed_password = get_password_hash(user.password)
        db_user = Auth(
            email=user.email,
            hashed_password=hashed_password
        )
        return await self.auth_repository.create_user(db_user)

