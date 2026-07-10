"""create assignments tables

Revision ID: d275374ad846
Revises: f455fb077ab6
Create Date: 2026-07-10 17:40:58.781205

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd275374ad846'
down_revision: Union[str, Sequence[str], None] = 'f455fb077ab6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
