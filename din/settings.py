from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.engine import create_engine


class Base(DeclarativeBase):
    pass


DB_URL = 'sqlite:///sqlite.db'
DB_BASE = Base
DB = create_engine(DB_URL)
Session = sessionmaker(bind=DB)
