import pytest

from events_app import db, create_app
from events_app.auth import create_admin_user

@pytest.fixture
def app():
    test_data_dir = 'tests/data'

    app = create_app(mode='test')

    with app.app_context():
        db.drop_all()
        db.create_all()

        create_admin_user()

        yield app

        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

