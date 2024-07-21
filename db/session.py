from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from core.config import settings

engine = create_async_engine(settings.pg_dsn)


async def get_session() -> AsyncSession:
    """

    :return: Возвращает асинхронную сессию
    """
    async_session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session_maker() as session:
        yield session
