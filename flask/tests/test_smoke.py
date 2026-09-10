from models import db, Event
from datetime import date, time
import pytest
from app import create_app

@pytest.fixture()
def app():
    app = create_app(mode="test")

    with app.app_context():
        db.drop_all()
        db.create_all()

    yield app

@pytest.fixture()
def client(app):
    return app.test_client()

def test_request_example(client):
    response = client.get("/")
    assert b"Welcome to the Community Calendar!" in response.data