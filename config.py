import os
from pydantic import PostgresDsn

from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    db_name: str = os.getenv('DB_NAME')
    db_user: str = os.getenv('DB_USER')
    db_password: str = os.getenv('DB_PASSWORD')
    db_host: str = os.getenv('DB_HOST')
    db_port: str = os.getenv('DB_PORT')

    pg_dsn: PostgresDsn = f'postgres+asyncpg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'


settings = Settings()
