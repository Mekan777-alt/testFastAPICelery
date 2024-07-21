from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from books.controllers import router as books_router


async def on_startup():
    app.include_router(books_router, prefix="/api/v1", tags=["Books"])


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
