from enum import Enum


class BookingStatus(str, Enum):
    ACTIVE = 'active'
    RETURNED = 'returned'
    CANCELLED = 'cancelled'
