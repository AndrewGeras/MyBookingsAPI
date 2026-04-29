"""added uq_contr into rooms

Revision ID: eed9353c3ee7
Revises: c9e5d4615cf1
Create Date: 2026-04-27 13:13:54.061561

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "eed9353c3ee7"
down_revision: Union[str, Sequence[str], None] = "c9e5d4615cf1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_unique_constraint("uq_hotel_id_title", "rooms", ["hotel_id", "title"])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("uq_hotel_id_title", "rooms", type_="unique")
