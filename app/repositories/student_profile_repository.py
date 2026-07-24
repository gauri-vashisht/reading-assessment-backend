from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload
from app.models.user import User
from app.models.student_profile import StudentProfile
from app.repositories.base_repository import BaseRepository


class StudentProfileRepository(
    BaseRepository[StudentProfile]
):

    def __init__(self):
        super().__init__(StudentProfile)

    def get_all(
        self,
        db: Session,
        classroom_id=None,
    ):
        stmt = (
            select(StudentProfile)
            .join(User, StudentProfile.user_id == User.id)
            .options(
                joinedload(StudentProfile.user)
            )
        )

        if classroom_id is not None:
            stmt = stmt.where(
                StudentProfile.classroom_id == classroom_id
            )

        stmt = stmt.order_by(
            User.full_name
        )

        return db.scalars(stmt).all()

    def get_by_user(
        self,
        db: Session,
        user_id,
    ):
        stmt = select(StudentProfile).where(
            StudentProfile.user_id == user_id
        )

        return db.scalar(stmt)

    def get_by_admission_number(
        self,
        db: Session,
        school_id,
        admission_number,
    ):
        stmt = select(StudentProfile).where(
            StudentProfile.school_id == school_id,
            StudentProfile.admission_number == admission_number,
        )

        return db.scalar(stmt)

    def get_by_roll_number(
        self,
        db: Session,
        classroom_id,
        roll_number,
    ):
        stmt = select(StudentProfile).where(
            StudentProfile.classroom_id == classroom_id,
            StudentProfile.roll_number == roll_number,
        )

        return db.scalar(stmt)

    def get_by_id(
        self,
        db: Session,
        profile_id,
    ):
        stmt = select(StudentProfile).where(
            StudentProfile.id == profile_id
        )

        return db.scalar(stmt)

    def update(
        self,
        db: Session,
        student: StudentProfile,
        data: dict,
    ):
        for key, value in data.items():
            setattr(student, key, value)

        db.flush()
        db.refresh(student)

        return student


student_profile_repository = StudentProfileRepository()