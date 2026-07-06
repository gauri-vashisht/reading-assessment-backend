from enum import Enum


class UserRole(str, Enum):

    ADMIN = "admin"

    TEACHER = "teacher"

    STUDENT = "student"

class ReadingDifficulty(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class AssessmentStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"