from sqlalchemy import String, Date, DateTime, func, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from app.db.base import Base
from datetime import datetime, date


if TYPE_CHECKING:
    from app.models.user import User

class Dashboard(Base): 
  __tablename__ = "dashboard"

  id: Mapped[int] = mapped_column(primary_key=True)
  user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
  total_applications: Mapped[int] = mapped_column(default=0)
  pending_applications: Mapped[int] = mapped_column(default=0)
  interviewing: Mapped[int] = mapped_column(default=0)
  offers: Mapped[int] = mapped_column(default=0)
  created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
  interview_rate: Mapped[float] = mapped_column(default=0.0)
  offer_rate: Mapped[float] = mapped_column(default=0.0)
  