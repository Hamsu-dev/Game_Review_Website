from pathlib import Path
import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers

from games.adapters import database_repository
from games.adapters.orm import metadata, map_model_to_tables

TEST_DATA_PATH = Path('games') / '..' / 'tests' / 'data'

TEST_DATABASE_URI_IN_MEMORY = 'sqlite://'
TEST_DATABASE_URI_FILE = 'sqlite:///test_games.db'

@pytest.fixture
def database_engine():
    clear_mappers()
    engine = create_engine(TEST_DATABASE_URI_FILE)
    metadata.create_all(engine)
    for table in reversed(metadata.sorted_tables):
        engine.execute(table.delete())
    map_model_to_tables()

    session_factory = sessionmaker(autocommit=False, autoflush=True, bind=engine)
    repo_instance = database_repository.DatabaseRepository(session_factory)
    database_repository.populate(TEST_DATA_PATH, repo_instance)
    yield engine
    metadata.drop_all(engine)

@pytest.fixture
def session_factory():
    clear_mappers()
    engine = create_engine(TEST_DATABASE_URI_IN_MEMORY)
    metadata.create_all(engine)
    for table in reversed(metadata.sorted_tables):
        engine.execute(table.delete())
    map_model_to_tables()

    session_factory = sessionmaker(autocommit=False, autoflush=True, bind=engine)
    repo_instance = database_repository.DatabaseRepository(session_factory)
    database_repository.populate(TEST_DATA_PATH, repo_instance)
    yield session_factory
    metadata.drop_all(engine)

@pytest.fixture
def empty_session():
    clear_mappers()
    engine = create_engine(TEST_DATABASE_URI_IN_MEMORY)
    metadata.create_all(engine)
    for table in reversed(metadata.sorted_tables):
        engine.execute(table.delete())
    map_model_to_tables()
    
    session_factory = sessionmaker(bind=engine)
    yield session_factory()
    metadata.drop_all(engine)