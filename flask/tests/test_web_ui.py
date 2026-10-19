from models import Event, db
from datetime import date, time
from sqlalchemy import select

def test_request_example(client):
    response = client.get("/")
    assert b"Welcome to the Community Calendar" in response.data

def test_list_events(client):
    response = client.get("/list_events")
    assert response.status_code == 200

def test_add_and_update_event(app, client):
    response = client.post("/add_event", data={
        "title": "Web event",
        "date": "2026-10-19",
        "time": "13:35",
    })
    assert response.status_code == 200

    with app.app_context():
        saved_event = db.session.scalar(select(Event).order_by(Event.id))

        assert saved_event.title == "Web event"
        assert saved_event.date == date(2026, 10, 19)
        assert saved_event.time == time(hour=13, minute=35, second=0)
        assert saved_event.id == 1

        event_id = saved_event.id

    response = client.post("/update_event/{0}".format(event_id), data={
        "title": "My Event",
        "date": "2026-10-19",
        "time": "14:20"
    })

    response = client.get("/list_events")
    assert b'My Event' in response.data
    assert response.status_code == 200
