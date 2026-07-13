"""create audio recordings table

Revision ID: 6f46a3130a45
Revises: 3492eeaaaab5
Create Date: 2026-07-13 12:36:11.308528

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = "6f46a3130a45"
down_revision = "3492eeaaaab5"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "audio_recordings",

        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),

        sa.Column(
            "assignment_id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),

        sa.Column(
            "student_profile_id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),

        sa.Column(
            "bucket_name",
            sa.String(length=100),
            nullable=False,
        ),

        sa.Column(
            "object_key",
            sa.String(length=500),
            nullable=False,
        ),

        sa.Column(
            "original_filename",
            sa.String(length=255),
            nullable=False,
        ),

        sa.Column(
            "content_type",
            sa.String(length=100),
            nullable=False,
        ),

        sa.Column(
            "file_size_bytes",
            sa.BigInteger(),
            nullable=False,
        ),

        sa.Column(
            "duration_seconds",
            sa.Integer(),
            nullable=True,
        ),

        sa.Column(
            "uploaded_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),

        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),

        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            onupdate=sa.func.now(),
            nullable=False,
        ),
        
        sa.Column(
            "checksum",
            sa.String(length=64),
            nullable=True,
        ),

        sa.ForeignKeyConstraint(
            ["assignment_id"],
            ["reading_assignments.id"],
            ondelete="CASCADE",
        ),

        sa.ForeignKeyConstraint(
            ["student_id"],
            ["student_profiles.id"],
            ondelete="CASCADE",
        ),

        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("object_key"),
    )

    op.create_index(
        op.f("ix_audio_recordings_assignment_id"),
        "audio_recordings",
        ["assignment_id"],
    )

    op.create_index(
        op.f("ix_audio_recordings_student_profile_id"),
        "audio_recordings",
        ["student_id"],
    )


def downgrade() -> None:
    op.drop_index(
        op.f("ix_audio_recordings_student_id"),
        table_name="audio_recordings",
    )

    op.drop_index(
        op.f("ix_audio_recordings_assignment_id"),
        table_name="audio_recordings",
    )

    op.drop_table("audio_recordings")