from sqlalchemy import String, Date, DateTime, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base 

class Application(Base): 
  __tablename__ = "applications" 

  id: Mapped[int] = mapped_column(primary_key=True, index=True)
  user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
  company: Mapped[str] = mapped_column(String(255))
  role_title: Mapped[str] = mapped_column(String(255))
  date_applied: Mapped[Date] = mapped_column(Date)
  status: Mapped[str] = mapped_column(Enum("APPLIED", "INTERVIEWING", "OFFER", "REJECTED", name="application_status"))
  created_at: Mapped[DateTime] = mapped_column(DateTime)
  updated_at: Mapped[DateTime] = mapped_column(DateTime)

