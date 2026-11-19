import pytest

from events_app import db, create_app
from events_app.auth import create

@pytest.fixture
def app():

    app = create_app(mode='test')

    with app.app_context():
        db.drop_all()
        db.create_all()

        create()

        yield app

        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

