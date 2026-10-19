from models import db, Event
from datetime import date, time
from sqlalchemy import select

def test_event_persistence(app):
    with app.app_context():
        event = Event(
            title="Test Event",
            date=date(2026, 8, 5),
            time=time(hour=10, minute=15, second=33),
        )

        db.session.add(event)
        db.session.commit()

        saved_event = db.session.scalar(select(Event).order_by(Event.id))

        assert saved_event is not None
        assert saved_event.title == "Test Event"
        assert saved_event.date == date(2026, 8, 5)
        assert saved_event.time == time(hour=10, minute=15, second=33)

def test_long_event_name_persistence(app):
    with app.app_context():
        event = Event(
            title='A very long event name', 
            date=date(2026, 8, 5),
            time=time(hour=10, minute=15, second=33)
        )
        
        db.session.add(event)
        db.session.commit()

        saved_event = db.session.scalar(select(Event).order_by(Event.id))

        assert saved_event is not None
        assert saved_event.title == 'A very long event name'
        assert saved_event.date == date(2026, 8, 5)
        assert saved_event.time == time(hour=10, minute=15, second=33)

    