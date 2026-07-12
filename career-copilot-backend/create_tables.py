from app.db.session import engine
from app.db.base import Base
import app.models  # noqa: F401 - registers every model with SQLAlchemy

Base.metadata.create_all(bind=engine)
print("Tables created.")
