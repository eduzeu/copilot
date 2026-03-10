from __future__ import annotations
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.user import User


class CoachSession(Base):
    __tablename__ = "coach_sessions"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True, nullable=False)

    resume_id: Mapped[int] = mapped_column(ForeignKey("resumes.id"), index=True, nullable=False)
    application_id: Mapped[int] = mapped_column(ForeignKey("applications.id"), index=True, nullable=False)

    question_type: Mapped[str] = mapped_column(String(50), nullable=False)  # technical / behavioral / system_design / mixed
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    questions: Mapped[list["CoachQuestion"]] = relationship(
        "CoachQuestion",
        back_populates="session",
        cascade="all, delete-orphan"
    )


class CoachQuestion(Base):
    __tablename__ = "coach_questions"

    id: Mapped[int] = mapped_column(primary_key=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("coach_sessions.id"), index=True, nullable=False)

    question_type: Mapped[str] = mapped_column(String(50), nullable=False)
    question_text: Mapped[str] = mapped_column(Text, nullable=False)
    reason: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    session: Mapped["CoachSession"] = relationship("CoachSession", back_populates="questions")