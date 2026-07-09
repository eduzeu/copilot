from sqlalchemy import text
from app.db.session import engine

with engine.begin() as conn:
    conn.execute(text("DROP TABLE IF EXISTS applications CASCADE"))

print("Dropped applications table.")