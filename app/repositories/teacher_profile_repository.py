from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.teacher_profile import TeacherProfile
from app.repositories.base_repository import BaseRepository


class TeacherProfileRepository(
    BaseRepository[TeacherProfile]
):

    def __init__(self):
        super().__init__(TeacherProfile)

    def get_by_user(
        self,
        db: Session,
        user_id,
    ):
        stmt = select(TeacherProfile).where(
            TeacherProfile.user_id == user_id
        )

        return db.scalar(stmt)

    def get_by_employee_id(
        self,
        db: Session,
        school_id,
        employee_id,
    ):
        stmt = select(TeacherProfile).where(
            TeacherProfile.school_id == school_id,
            TeacherProfile.employee_id == employee_id,
        )

        return db.scalar(stmt)

    def update(
        self,
        db: Session,
        teacher: TeacherProfile,
        data: dict,
    ):

        for key, value in data.items():
            setattr(teacher, key, value)

        db.flush()
        db.refresh(teacher)

        return teacher


teacher_profile_repository = TeacherProfileRepository()