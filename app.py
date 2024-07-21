from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from db.base import Base
from db.session import engine


async def on_startup():
    pass


app = FastAPI(
    title="Test FastAPI Celery Project",
    description="This is a test FastAPI Celery Project",
    on_startup=[on_startup]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
