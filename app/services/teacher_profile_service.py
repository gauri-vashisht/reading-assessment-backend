from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.enums.user_role import UserRole
from app.models.teacher_profile import TeacherProfile
from app.repositories.classroom_repository import classroom_repository
from app.repositories.school_repository import school_repository
from app.repositories.teacher_profile_repository import (
    teacher_profile_repository,
)
from app.repositories.user_repository import user_repository
from app.schemas.teacher_profile import (
    TeacherProfileCreate,
    TeacherProfileUpdate,
)


class TeacherProfileService:

    def create_teacher_profile(
        self,
        db: Session,
        data: TeacherProfileCreate,
    ):

        user = user_repository.get_by_id(
            db,
            data.user_id,
        )

        if user is None:
            raise HTTPException(404, "User not found.")

        if user.role != UserRole.TEACHER:
            raise HTTPException(
                400,
                "User must have TEACHER role.",
            )

        if teacher_profile_repository.get_by_user(
            db,
            data.user_id,
        ):
            raise HTTPException(
                400,
                "Teacher profile already exists.",
            )

        if school_repository.get_by_id(
            db,
            data.school_id,
        ) is None:
            raise HTTPException(
                404,
                "School not found.",
            )

        if data.classroom_id:

            if classroom_repository.get_by_id(
                db,
                data.classroom_id,
            ) is None:
                raise HTTPException(
                    404,
                    "Classroom not found.",
                )

        if teacher_profile_repository.get_by_employee_id(
            db,
            data.school_id,
            data.employee_id,
        ):
            raise HTTPException(
                400,
                "Employee ID already exists.",
            )

        teacher = TeacherProfile(
            **data.model_dump()
        )

        return teacher_profile_repository.create(
            db,
            teacher,
        )

    def get_teacher_profiles(
        self,
        db: Session,
    ):
        return teacher_profile_repository.get_all(db)

    def get_teacher_profile(
        self,
        db: Session,
        teacher_id: UUID,
    ):
        teacher = teacher_profile_repository.get_by_id(
            db,
            teacher_id,
        )

        if teacher is None:
            raise HTTPException(
                404,
                "Teacher profile not found.",
            )

        return teacher

    def update_teacher_profile(
        self,
        db: Session,
        teacher_id: UUID,
        data: TeacherProfileUpdate,
    ):
        teacher = self.get_teacher_profile(
            db,
            teacher_id,
        )

        return teacher_profile_repository.update(
            db,
            teacher,
            data.model_dump(exclude_unset=True),
        )

    def delete_teacher_profile(
        self,
        db: Session,
        teacher_id: UUID,
    ):
        teacher = self.get_teacher_profile(
            db,
            teacher_id,
        )

        teacher_profile_repository.delete(
            db,
            teacher,
        )


teacher_profile_service = TeacherProfileService()