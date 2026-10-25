import pytest, shutil

from models import db
from app import create_app

@pytest.fixture
def app():
    test_data_dir = 'tests/data'

    # shutil.rmtree(test_data_dir, ignore_errors = True)

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