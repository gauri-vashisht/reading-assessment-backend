"""create reading assignment tables

Revision ID: 3492eeaaaab5
Revises: d275374ad846
Create Date: 2026-07-10 17:49:28.035308

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '3492eeaaaab5'
down_revision: Union[str, Sequence[str], None] = 'd275374ad846'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    assignment_status = sa.Enum(
        "PENDING",
        "COMPLETED",
        name="assignment_status",
    )


    op.create_table(
        "reading_assignments",

        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            nullable=False,
        ),

        sa.Column(
            "passage_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey(
                "reading_passages.id",
                ondelete="CASCADE",
            ),
            nullable=False,
        ),

        sa.Column(
            "classroom_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey(
                "classrooms.id",
                ondelete="CASCADE",
            ),
            nullable=True,
        ),

        sa.Column(
            "assigned_by",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey(
                "users.id",
            ),
            nullable=False,
        ),

        sa.Column(
            "due_date",
            sa.DateTime(timezone=True),
            nullable=True,
        ),

        sa.Column(
            "remarks",
            sa.Text(),
            nullable=True,
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
            nullable=False,
        ),
    )

    op.create_table(
        "student_assignments",

        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            nullable=False,
        ),

        sa.Column(
            "assignment_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey(
                "reading_assignments.id",
                ondelete="CASCADE",
            ),
            nullable=False,
        ),

        sa.Column(
            "student_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey(
                "users.id",
                ondelete="CASCADE",
            ),
            nullable=False,
        ),

        sa.Column(
            "status",                     
            assignment_status,
            nullable=False,
            server_default="PENDING",
        ),

        sa.Column(
            "completed_at",
            sa.DateTime(timezone=True),
            nullable=True,
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
            nullable=False,
        ),
    )

    op.create_index(
        "ix_ra_passage",
        "reading_assignments",
        ["passage_id"],
    )

    op.create_index(
        "ix_ra_classroom",
        "reading_assignments",
        ["classroom_id"],
    )

    op.create_index(
        "ix_sa_assignment",
        "student_assignments",
        ["assignment_id"],
    )

    op.create_index(
        "ix_sa_student",
        "student_assignments",
        ["student_id"],
    )

    op.create_index(
        "ix_sa_status",
        "student_assignments",
        ["status"],
    )

def downgrade() -> None:

    op.drop_index(
        "ix_sa_status",
        table_name="student_assignments",
    )

    op.drop_index(
        "ix_sa_student",
        table_name="student_assignments",
    )

    op.drop_index(
        "ix_sa_assignment",
        table_name="student_assignments",
    )

    op.drop_table(
        "student_assignments",
    )

    op.drop_index(
        "ix_ra_classroom",
        table_name="reading_assignments",
    )

    op.drop_index(
        "ix_ra_passage",
        table_name="reading_assignments",
    )

    op.drop_table(
        "reading_assignments",
    )

    sa.Enum(
        name="assignment_status",
    ).drop(
        op.get_bind(),
        checkfirst=True,
    )
