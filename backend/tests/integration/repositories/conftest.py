import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from testcontainers.postgres import PostgresContainer

from sightcall_transcript_to_tutorial.infrastructure.for_production.models.base import Base


@pytest.fixture(scope="session")
def pg_session():
    with PostgresContainer("postgres:17") as pg:
        engine = create_engine(pg.get_connection_url())
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()
        try:
            yield session
        finally:
            session.close()
            Base.metadata.drop_all(engine)
