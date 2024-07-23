from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from books.controllers import router as books_router
from auth.controllers import router as auth_router
from booking.controllers import router as booking_router
from genres.controllers import router as genres_router
from authors.controllers import router as authors_router


async def on_startup():
    app.include_router(books_router, prefix="/api/v1", tags=["Books"])
    app.include_router(auth_router, prefix="/api/v1", tags=["Auth and Registration"])
    app.include_router(booking_router, prefix="/api/v1", tags=["Booking"])
    app.include_router(genres_router, prefix="/api/v1", tags=["Genres"])
    app.include_router(authors_router, prefix="/api/v1", tags=["Authors"])

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
