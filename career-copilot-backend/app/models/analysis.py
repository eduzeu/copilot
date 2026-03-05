from __future__ import annotations
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
  from app.models.user import User
  from app.models.resume import Resume


class Analysis(Base): 
  __tablename__ = "analysis" 

  id: Mapped[int] = mapped_column(primary_key=True)
  user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True, nullable=False)
  
  resume_id: Mapped[int] = mapped_column(ForeignKey("resumes.id"), index=True, nullable=False)
  application_id: Mapped[int | None] = mapped_column(Integer, nullable=True)

  job_title: Mapped[str | None] = mapped_column(String(255), nullable=True)
  job_description: Mapped[str] = mapped_column(Text, nullable=False)

  created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

  bullets: Mapped[list["AnalysisBullet"]] = relationship(
      back_populates="run",
      cascade="all, delete-orphan"
  )

class AnalysisBullet(Base):
    __tablename__ = "analysis_bullets"

    id: Mapped[int] = mapped_column(primary_key=True)
    run_id: Mapped[int] = mapped_column(ForeignKey("analysis.id"), index=True, nullable=False)

    bullet_index: Mapped[int] = mapped_column(Integer, nullable=False)
    original_text: Mapped[str] = mapped_column(Text, nullable=False)

    relevance_score: Mapped[int] = mapped_column(Integer, nullable=False, default=0)  # 0–100
    feedback: Mapped[str | None] = mapped_column(Text, nullable=True)
    rewrite_ats: Mapped[str | None] = mapped_column(Text, nullable=True)
    rewrite_strong: Mapped[str | None] = mapped_column(Text, nullable=True)

    missing_keywords_csv: Mapped[str | None] = mapped_column(Text, nullable=True)  # store as "aws,react,redis"

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    run: Mapped["Analysis"] = relationship(back_populates="bullets")
  

