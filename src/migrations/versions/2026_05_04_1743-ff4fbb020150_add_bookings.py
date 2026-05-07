"""add_bookings

Revision ID: ff4fbb020150
Revises: eed9353c3ee7
Create Date: 2026-05-04 17:43:33.623442

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "ff4fbb020150"
down_revision: Union[str, Sequence[str], None] = "eed9353c3ee7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "bookings",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("room_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("date_from", sa.Date(), nullable=False),
        sa.Column("date_to", sa.Date(), nullable=False),
        sa.Column("price", sa.Numeric(precision=8, scale=2), nullable=False),
        sa.CheckConstraint("date_to > date_from", name="check_booking_duration"),
        sa.ForeignKeyConstraint(
            ["room_id"],
            ["rooms.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("bookings")
