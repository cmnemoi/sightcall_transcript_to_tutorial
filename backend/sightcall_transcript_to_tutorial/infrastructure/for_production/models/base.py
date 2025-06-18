from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from sightcall_transcript_to_tutorial.domain.config.settings import settings


class Base(DeclarativeBase):
    pass


# SQLAlchemy engine and session factory for production use
engine = create_engine(settings.database_url, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
