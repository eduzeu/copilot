"""Backward-compatible migration entrypoint.

Use `alembic upgrade head` directly for new automation.
"""

from alembic import command
from alembic.config import Config
from sqlalchemy import inspect

from app.db.session import engine

config = Config("alembic.ini")
tables = set(inspect(engine).get_table_names())
if "users" in tables and "alembic_version" not in tables:
    # Databases created by the previous Base.metadata.create_all workflow already
    # contain the baseline schema. Mark that baseline before applying new changes.
    command.stamp(config, "80039962503f")
command.upgrade(config, "head")
print("Database schema is current.")
