# app/database/models.py

from app.models.user import User
from app.models.school import School

# Future models (enable when implemented)
# from app.models.academic_year import AcademicYear
# from app.models.classroom import Classroom
# from app.models.teacher_profile import TeacherProfile
# from app.models.student_profile import StudentProfile

__all__ = [
    "User",
    "School",
]