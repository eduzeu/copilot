from enum import Enum
from sqlalchemy import Column, Date, ForeignKey, Integer, String, DateTime, func
from sqlalchemy.orm import Mapped, relationship
from typing import TYPE_CHECKING

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.user import User


class ApplicationStatus(str, Enum):
    APPLIED = "applied"
    PENDING = "pending"
    INTERVIEW = "interview"
    ACCEPTED = "accepted"
    REJECTED = "rejected"


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    company = Column(String, nullable=False)
    role_title = Column(String, nullable=False)
    location = Column(String, nullable=False)
    job_posting_url = Column(String, nullable=True)
    date_applied = Column(Date, nullable=False)
    status = Column(String, nullable=False, default=ApplicationStatus.APPLIED.value)
    notes = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    owner: Mapped["User"] = relationship(back_populates="applications")