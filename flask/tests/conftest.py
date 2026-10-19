import pytest

from models import db
from app import create_app

@pytest.fixture
def app():
    app = create_app(mode='test')

    with app.app_context():
        db.drop_all()
        db.create_all()

        yield app

        db.session.remove()
        db.drop_all()

@pytest.fixture()
def client(app):
    return app.test_client()