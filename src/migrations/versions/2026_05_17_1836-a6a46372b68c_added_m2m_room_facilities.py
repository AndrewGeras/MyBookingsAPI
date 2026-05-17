"""added M2M room_facilities

Revision ID: a6a46372b68c
Revises: ff4fbb020150
Create Date: 2026-05-17 18:36:24.415984

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "a6a46372b68c"
down_revision: Union[str, Sequence[str], None] = "ff4fbb020150"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "facilities",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "room_facilities",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("room_id", sa.Integer(), nullable=False),
        sa.Column("facility_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["facility_id"],
            ["facilities.id"],
        ),
        sa.ForeignKeyConstraint(
            ["room_id"],
            ["rooms.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("room_id", "facility_id", name="uq_room_facility"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("room_facilities")
    op.drop_table("facilities")
