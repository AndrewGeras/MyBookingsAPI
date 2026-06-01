from src.models.bookings import BookingsORM
from src.models.facilities import FacilitiesORM, RoomFacilitiesORM
from src.models.hotels import HotelsORM
from src.models.rooms import RoomsORM
from src.models.users import UsersORM
from src.repositories.mappers.base import DataMapper
from src.schemas.hotels import Hotel, AvailableHotel
from src.schemas.rooms import Room, RoomAvailable
from src.schemas.users import User, UserWithHashedPassword
from src.schemas.bookings import Booking
from src.schemas.facilities import Facility, RoomFacility


class HotelMapper(DataMapper[HotelsORM, Hotel]):
    db_model = HotelsORM
    schema = Hotel


class AvailableHotelMapper(HotelMapper):
    schema = AvailableHotel


class RoomMapper(DataMapper[RoomsORM, Room]):
    db_model = RoomsORM
    schema = Room


class RoomAvailableMapper(RoomMapper):
    schema = RoomAvailable


class UserMapper(DataMapper[UsersORM, User]):
    db_model = UsersORM
    schema = User


class UserWithHashedPasswordMapper(UserMapper):
    schema = UserWithHashedPassword


class BookingMapper(DataMapper[BookingsORM, Booking]):
    db_model = BookingsORM
    schema = Booking


class FacilityMapper(DataMapper[FacilitiesORM, Facility]):
    db_model = FacilitiesORM
    schema = Facility


class RoomFacilityMapper(DataMapper[RoomFacilitiesORM, RoomFacility]):
    db_model = RoomFacilitiesORM
    schema = RoomFacility
