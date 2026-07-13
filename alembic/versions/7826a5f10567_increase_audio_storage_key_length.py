"""increase audio storage_key length

Revision ID: 7826a5f10567
Revises: 67bf575b07ea
Create Date: 2026-07-13 17:30:06.941037

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7826a5f10567'
down_revision: Union[str, Sequence[str], None] = '67bf575b07ea'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
