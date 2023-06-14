
from alembic import command
from alembic.config import Config
from src.db.database import engine
from sqlalchemy import inspect

def check_if_table_exist():
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    return bool(tables)

if not check_if_table_exist():
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")