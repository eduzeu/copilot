from enum import Enum

class ApplicationStatus(str, Enum):
    PENDING = "PENDING"
    INTERVIEWING = "INTERVIEWING"
    OFFER = "OFFER"
    REJECTED = "REJECTED"
