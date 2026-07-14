"""add assessment word lists

Revision ID: b02a5c8df9ef
Revises: cd0486c50e93
Create Date: 2026-07-14 16:53:09.064598

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'b02a5c8df9ef'
down_revision: Union[str, Sequence[str], None] = 'cd0486c50e93'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


from sqlalchemy.dialects.postgresql import JSONB

def upgrade():

    op.add_column(
        "assessment_results",
        sa.Column(
            "incorrect_word_list",
            JSONB,
            nullable=False,
            server_default=sa.text("'[]'::jsonb"),
        ),
    )

    op.add_column(
        "assessment_results",
        sa.Column(
            "skipped_word_list",
            JSONB,
            nullable=False,
            server_default=sa.text("'[]'::jsonb"),
        ),
    )

    op.add_column(
        "assessment_results",
        sa.Column(
            "extra_word_list",
            JSONB,
            nullable=False,
            server_default=sa.text("'[]'::jsonb"),
        ),
    )


def downgrade():

    op.drop_column(
        "assessment_results",
        "extra_word_list",
    )

    op.drop_column(
        "assessment_results",
        "skipped_word_list",
    )

    op.drop_column(
        "assessment_results",
        "incorrect_word_list",
    )