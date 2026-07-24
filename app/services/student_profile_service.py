from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.enums.user_role import UserRole
from app.models.student_profile import StudentProfile
from app.repositories.classroom_repository import classroom_repository
from app.repositories.school_repository import school_repository
from app.repositories.student_profile_repository import student_profile_repository
from app.repositories.user_repository import user_repository
from app.schemas.student_profile import (
    StudentProfileCreate,
    StudentProfileUpdate,
    StudentSummaryResponse
)


class StudentProfileService:

    def create_student_profile(
        self,
        db: Session,
        data: StudentProfileCreate,
    ):

        user = user_repository.get_by_id(
            db,
            data.user_id,
        )

        if user is None:
            raise HTTPException(
                404,
                "User not found.",
            )

        if user.role != UserRole.STUDENT:
            raise HTTPException(
                400,
                "User must have STUDENT role.",
            )

        if student_profile_repository.get_by_user(
            db,
            data.user_id,
        ):
            raise HTTPException(
                400,
                "Student profile already exists.",
            )

        if school_repository.get_by_id(
            db,
            data.school_id,
        ) is None:
            raise HTTPException(
                404,
                "School not found.",
            )

        if classroom_repository.get_by_id(
            db,
            data.classroom_id,
        ) is None:
            raise HTTPException(
                404,
                "Classroom not found.",
            )

        if student_profile_repository.get_by_admission_number(
            db,
            data.school_id,
            data.admission_number,
        ):
            raise HTTPException(
                400,
                "Admission number already exists.",
            )

        if student_profile_repository.get_by_roll_number(
            db,
            data.classroom_id,
            data.roll_number,
        ):
            raise HTTPException(
                400,
                "Roll number already exists.",
            )

        student = StudentProfile(
            **data.model_dump()
        )

        return student_profile_repository.create(
            db,
            student,
        )

    def get_students(
        self,
        db: Session,
        classroom_id: UUID | None = None,
        summary: bool = False,
    ):
        students = student_profile_repository.get_all(
            db,
            classroom_id=classroom_id,
        )

        if summary:
            return [
                StudentSummaryResponse(
                    id=student.user.id,
                    full_name=student.user.full_name,
                )
                for student in students
            ]

        return students

    def get_student(
        self,
        db: Session,
        student_id: UUID,
    ):

        student = student_profile_repository.get_by_id(
            db,
            student_id,
        )

        if student is None:
            raise HTTPException(
                404,
                "Student not found.",
            )

        return student

    def update_student(
        self,
        db: Session,
        student_id: UUID,
        data: StudentProfileUpdate,
    ):

        student = self.get_student(
            db,
            student_id,
        )

        return student_profile_repository.update(
            db,
            student,
            data.model_dump(
                exclude_unset=True,
            ),
        )

    def delete_student(
        self,
        db: Session,
        student_id: UUID,
    ):

        student = self.get_student(
            db,
            student_id,
        )

        student_profile_repository.delete(
            db,
            student,
        )


student_profile_service = StudentProfileService()