from enum import Enum


class ApplicationStatus(str, Enum):
    APPLIED = "applied"
    PENDING = "pending"
    INTERVIEW = "interview"
    ACCEPTED = "accepted"
    REJECTED = "rejected"