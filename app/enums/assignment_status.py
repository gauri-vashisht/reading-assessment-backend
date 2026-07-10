from enum import Enum


class AssignmentStatus(str, Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"