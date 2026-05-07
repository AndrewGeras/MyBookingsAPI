from decimal import Decimal
from datetime import date

from sqlalchemy.orm import mapped_column, Mapped, validates
from sqlalchemy import ForeignKey, Numeric
from sqlalchemy.schema import CheckConstraint
from sqlalchemy.ext.hybrid import hybrid_property

from src.database import Base


class BookingsORM(Base):
    __tablename__ = "bookings"
    __table_args__ = (CheckConstraint('date_to > date_from', name='check_booking_duration'),)

    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    date_from: Mapped[date]
    date_to: Mapped[date]
    price: Mapped[Decimal] = mapped_column(Numeric(precision=8, scale=2))

    @hybrid_property
    def total_cost(self) -> Decimal:
        return self.price * (self.date_to - self.date_from).days
