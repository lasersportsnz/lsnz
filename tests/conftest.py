
# Ensure project root is in sys.path for imports
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest
from app import create_app, db
from config import Config

class TestConfig(Config):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

@pytest.fixture(scope='session')
def app():
    app = create_app(TestConfig)
    return app

@pytest.fixture(scope='session')
def runner(app):
    return app.test_cli_runner()

@pytest.fixture(scope='function', autouse=True)
def setup_database(app):
    db.create_all()
    yield
    db.session.remove()
    db.drop_all()
