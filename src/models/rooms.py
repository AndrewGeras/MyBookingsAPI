from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base


class RoomsORM(Base):
    __tablename__ = "rooms"
    __table_args__ = (UniqueConstraint("hotel_id", "title", name="uq_hotel_id_title"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"))
    title: Mapped[str]
    description: Mapped[str | None]
    price: Mapped[Decimal] = mapped_column(Numeric(precision=8, scale=2))
    quantity: Mapped[int]
