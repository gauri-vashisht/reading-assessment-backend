# app/database/models.py

from app.models.user import User

__all__ = ["User"]


from app.models.school import School
from app.models.academic_year import AcademicYear
from app.models.classroom import Classroom

from app.models.teacher_profile import TeacherProfile
from app.models.student_profile import StudentProfile