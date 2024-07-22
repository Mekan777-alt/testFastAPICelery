from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from genres.schemas import GenreResponseSchema, GenreCreateUpdateSchema
from fastapi import APIRouter, Depends
from starlette import status

from db.session import get_session
from genres.services import GenreService

router = APIRouter()


@router.get('/genres', summary="Возвращает все жанры", status_code=status.HTTP_200_OK,
            response_model=List[GenreResponseSchema])
async def get_genres(session: AsyncSession = Depends(get_session)):
    """

    :return: Возвращает все созданные жанры соглсно схеме
    """

    service = GenreService(session)

    genres = await service.get_all_genres()

    return genres


@router.post('/genres', summary="Создать жанр", status_code=status.HTTP_201_CREATED,
             response_model=GenreResponseSchema)
async def create_new_genre(genre: GenreCreateUpdateSchema, session: AsyncSession = Depends(get_session)):
    """

    :param genre: Ожидает Имя жанра\n
    :return: Возвращает созданный экземпляр
    """

    service = GenreService(session)

    new_genre = await service.create_new_genre(genre)

    return new_genre


@router.get('/genres/{genre_id}', summary="Возвращает жанр по ID", status_code=status.HTTP_200_OK,
            response_model=GenreResponseSchema)
async def get_genre(genre_id: int, session: AsyncSession = Depends(get_session)):
    """

    :param genre_id: Принимает INT значение\n
    :return: Возвращает жанр согласно схеме
    """

    service = GenreService(session)

    genre = await service.get_genre(genre_id)

    return genre


@router.patch('/genres/{genre_id}', summary="Обновление имени жанра", response_model=GenreResponseSchema)
async def update_genre(genre_id: int, genre: GenreCreateUpdateSchema, session: AsyncSession = Depends(get_session)):
    """

    :param genre_id: Принимает INT значение\n
    :param genre: Принимает name в теле запроса\n
    :return: Возвращает обновленный ресурс
    """

    service = GenreService(session)

    genre = await service.update_genre(genre_id, genre)

    return genre


@router.delete('/genres/{genres_id}', summary="Удаление жанра", status_code=status.HTTP_204_NO_CONTENT)
async def delete_genre(genres_id: int, session: AsyncSession = Depends(get_session)):
    """

    :param genres_id: Принимает INT значение\n
    :return: При успешном удалении возвращает 204 статус No content
    """

    service = GenreService(session)

    await service.delete_genre(genres_id)
