from app.db.session import engine
from app.db.base import Base
from app.models.resume import Resume
from app.models.user import User
from app.models.application import Application

Base.metadata.create_all(bind=engine)
print("Tables created.")
