from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


if TYPE_CHECKING:
    from src.models.rooms import RoomsORM


class FacilitiesORM(Base):
    __tablename__ = "facilities"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))

    rooms: Mapped[list["RoomsORM"]] = relationship(
        secondary="room_facilities", back_populates="facilities"
    )


class RoomFacilitiesORM(Base):
    __tablename__ = "room_facilities"
    __table_args__ = (
        UniqueConstraint("room_id", "facility_id", name="uq_room_facility"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    facility_id: Mapped[int] = mapped_column(ForeignKey("facilities.id"))
