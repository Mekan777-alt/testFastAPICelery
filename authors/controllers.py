from fastapi import APIRouter, Depends, HTTPException, Form, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from db.session import get_session
from starlette import status
from typing import List
from authors.schemas import AuthorResponseSchemas
from authors.services import AuthorService

router = APIRouter()


@router.get('/authors', summary="Врзвращает всех авторов", status_code=status.HTTP_200_OK,
            response_model=List[AuthorResponseSchemas])
async def get_all_authors(session: AsyncSession = Depends(get_session)):
    """

    :return: Возвращает массив авторов согласно схеме
    """

    service = AuthorService(session)

    authors = await service.get_all_authors()
    return authors


@router.get('/authors/{author_id}', summary="Возвращает автора по ID", status_code=status.HTTP_200_OK,
            response_model=AuthorResponseSchemas)
async def get_author_by_id(author_id: int, session: AsyncSession = Depends(get_session)):
    """

    :param author_id: Принимает INT значение\n
    :return: Возвращает автора согласно схеме
    """
    service = AuthorService(session)

    author = await service.get_author(author_id)

    return author


@router.post('/authors', summary="Создание автора", status_code=status.HTTP_201_CREATED,
             response_model=AuthorResponseSchemas)
async def create_author(first_name: str = Form(...),
                        last_name: str = Form(...),
                        avatar: UploadFile = File(None),
                        session: AsyncSession = Depends(get_session)):
    """
    :param first_name: Принимает STR\n
    :param last_name: Принимает STR\n
    :param avatar: Принимает фотографию\n
    :return: Взвращает созданный экземпляр согласно схеме
    """

    service = AuthorService(session)

    new_author = await service.create_author(first_name=first_name, last_name=last_name, avatar=avatar)

    return new_author


@router.put('/authors/{author_id}', summary="Полное обновление данных автора", status_code=status.HTTP_200_OK,
            response_model=AuthorResponseSchemas)
async def all_update_authors(author_id: int,
                             first_name: str = Form(...),
                             last_name: str = Form(...),
                             avatar: UploadFile = File(...),
                             session: AsyncSession = Depends(get_session)):
    """

    :param last_name: Принимает STR\n
    :param author_id: Принимает INT значение\n
    :param first_name: Принимает STR\n
    :param avatar: Принимает фотографию\n
    :return: Взвращает обновленный экземпляр согласно схеме
    """

    service = AuthorService(session)

    update_authors = await service.update_author(author_id, first_name=first_name, last_name=last_name, avatar=avatar)

    return update_authors


@router.patch('/authors/{author_id}', summary="Частичное обновление данных автора", status_code=status.HTTP_200_OK,
              response_model=AuthorResponseSchemas)
async def partial_update_authors(author_id: int,
                                 first_name: str = Form(None),
                                 last_name: str = Form(None),
                                 avatar: UploadFile = File(None),
                                 session: AsyncSession = Depends(get_session)):
    """

    :param author_id: Принимает INT - обязательное поле\n
    :param first_name: Принимает STR - не обязательное поле\n
    :param last_name: Принимает STR - не обязательное поле\n
    :param avatar: Принимает фотографию - не обязательное поле\n
    :return: Взвращает обновленный экземпляр согласно схеме
    """

    service = AuthorService(session)

    update_authors = await service.partial_update_author(
        author_id,
        first_name=first_name,
        last_name=last_name,
        avatar=avatar
    )

    return update_authors


@router.delete('/authors/{author_id}', summary="Удаление автора", status_code=status.HTTP_204_NO_CONTENT)
async def delete_author(author_id: int, session: AsyncSession = Depends(get_session)):
    """

    :param author_id: Принимает INT значение
    :return: При успешном удалении возвращает 204 статус NO CONTENT
    """

    service = AuthorService(session)

    await service.delete_author(author_id)
