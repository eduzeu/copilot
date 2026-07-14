from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, JSON, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class CareerProfile(Base):
    __tablename__ = "career_profiles"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True, index=True)
    status: Mapped[str] = mapped_column(String(30), default="college")
    school: Mapped[str | None] = mapped_column(String(255), nullable=True)
    degree: Mapped[str | None] = mapped_column(String(255), nullable=True)
    major: Mapped[str | None] = mapped_column(String(255), nullable=True)
    current_year: Mapped[str | None] = mapped_column(String(50), nullable=True)
    graduation_year: Mapped[int | None] = mapped_column(Integer, nullable=True)
    current_role: Mapped[str | None] = mapped_column(String(255), nullable=True)
    years_experience: Mapped[int | None] = mapped_column(Integer, nullable=True)
    current_industry: Mapped[str | None] = mapped_column(String(255), nullable=True)

    experiences: Mapped[list] = mapped_column(JSON, default=list)
    technical_skills: Mapped[list] = mapped_column(JSON, default=list)
    dsa_level: Mapped[str] = mapped_column(String(30), default="not_started")
    system_design_level: Mapped[str] = mapped_column(String(30), default="not_started")
    behavioral_confidence: Mapped[str] = mapped_column(String(30), default="not_started")
    preferred_language: Mapped[str | None] = mapped_column(String(100), nullable=True)
    improvement_areas: Mapped[list] = mapped_column(JSON, default=list)
    certifications: Mapped[list] = mapped_column(JSON, default=list)

    target_roles: Mapped[list] = mapped_column(JSON, default=list)
    target_companies: Mapped[list] = mapped_column(JSON, default=list)
    target_industries: Mapped[list] = mapped_column(JSON, default=list)
    target_locations: Mapped[list] = mapped_column(JSON, default=list)
    position_types: Mapped[list] = mapped_column(JSON, default=list)
    workplace_preferences: Mapped[list] = mapped_column(JSON, default=list)
    application_timeline: Mapped[str | None] = mapped_column(String(255), nullable=True)
    primary_goal: Mapped[str | None] = mapped_column(Text, nullable=True)
    salary_expectations: Mapped[str | None] = mapped_column(String(255), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    owner = relationship("User", back_populates="career_profile")
