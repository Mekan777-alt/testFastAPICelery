from enum import Enum


class BookingStatus(str, Enum):
    ACTIVE = 'ACTIVE'
    RETURNED = 'RETURNED'
    CANCELLED = 'CANCELLED'
