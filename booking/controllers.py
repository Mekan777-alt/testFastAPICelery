from fastapi import APIRouter, Depends
from auth.models import Auth
from booking.schemas import BookingCreate, BookingResponse
from booking.services import BookingService
from db.session import get_session
from typing import Annotated, List
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession
from auth.dependencies import get_current_user

router = APIRouter()


@router.post('/books/{book_id}/booking', summary="Забронировать книгу", status_code=status.HTTP_201_CREATED,
             response_model=BookingResponse)
async def create_booking(book_id: int, booking: BookingCreate, current_user: Annotated[Auth, Depends(get_current_user)],
                         session: AsyncSession = Depends(get_session)):
    """
    :param current_user: Передавать access_token для идентификации пользователя переданный при авторизации\n
    :param book_id: Принимает INT значение книги\n
    :param booking: Принимает данные по схеме\n
    :return: Возвращает экзмепляр созданной брони
    """

    service = BookingService(session)

    created_booking = await service.create_booking(booking=booking, book_id=book_id, user_id=current_user.id)

    return created_booking


@router.get('/bookings', summary="Возвращает все забронированные книги пользователя",
            status_code=status.HTTP_200_OK, response_model=List[BookingResponse])
async def get_user_bookings(current_user: Annotated[Auth, Depends(get_current_user)],
                            session: AsyncSession = Depends(get_session)):
    """
    :param current_user: Передавать access_token для идентификации пользователя переданный при авторизации\n
    :return: Возвращает все забронированные книги пользователя
    """

    service = BookingService(session)
    bookings = await service.get_bookings_user(current_user.id)

    return bookings


@router.get('/bookings/{booking_id}', summary="Возвращает бронь по ID", response_model=BookingResponse,
            status_code=status.HTTP_200_OK)
async def get_booking_by_id(booking_id: int, current_user: Annotated[Auth, Depends(get_current_user)],
                            session: AsyncSession = Depends(get_session)):
    """

    :param booking_id: Принимает INT значение определенной брони\n
    :param current_user: Передавать access_token для идентификации пользователя переданный при авторизации\n
    :return: Возвращает определенную бронь согласно схеме
    """
    service = BookingService(session)

    booking = await service.get_bookings_id(booking_id=booking_id)

    return booking


@router.post('/booking/{booking_id}/return', summary="Сдать книгу", status_code=status.HTTP_200_OK,
             response_model=BookingResponse)
async def update_booking_to_user(booking_id: int, current_user: Annotated[Auth, Depends(get_current_user)],
                                 session: AsyncSession = Depends(get_session)):
    """
    :param booking_id: Принимает INT значение определенной брони\n
    :param current_user: Передавать access_token для идентификации пользователя переданный при авторизации\n
    :return: Возвращает обновленное бронирование
    """
    service = BookingService(session)
    updated_booking = await service.return_booking(booking_id)

    return updated_booking



