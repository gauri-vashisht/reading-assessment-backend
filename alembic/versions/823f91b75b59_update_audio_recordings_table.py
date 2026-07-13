"""update audio recordings table

Revision ID: 823f91b75b59
Revises: 6f46a3130a45
Create Date: 2026-07-13 16:51:54.337284

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '823f91b75b59'
down_revision: Union[str, Sequence[str], None] = '6f46a3130a45'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.alter_column(
        "audio_recordings",
        "object_name",
        new_column_name="storage_key",
    )

    op.alter_column(
        "audio_recordings",
        "file_name",
        new_column_name="original_filename",
    )

    op.alter_column(
        "audio_recordings",
        "file_size",
        new_column_name="file_size_bytes",
        type_=sa.BigInteger(),
    )

    op.alter_column(
        "audio_recordings",
        "student_id",
        new_column_name="student_profile_id",
    )

    op.add_column(
        "audio_recordings",
        sa.Column(
            "checksum",
            sa.String(length=64),
            nullable=True,
        ),
    )


def downgrade():
    op.drop_column(
        "audio_recordings",
        "checksum",
    )

    op.alter_column(
        "audio_recordings",
        "student_profile_id",
        new_column_name="student_id",
    )

    op.alter_column(
        "audio_recordings",
        "file_size_bytes",
        new_column_name="file_size",
        type_=sa.Integer(),
    )

    op.alter_column(
        "audio_recordings",
        "original_filename",
        new_column_name="file_name",
    )

    op.alter_column(
        "audio_recordings",
        "storage_key",
        new_column_name="object_name",
    )