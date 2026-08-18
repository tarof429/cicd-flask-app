from models import db, Event
from datetime import date, time

from app import create_app

def test_event_persistence():
    """
    GIVEN a Event model
    WHEN a new Event is saved to the database
    THEN check the title is saved correctly
    """

    app = create_app(mode='test')

    with app.app_context():
        db.drop_all()
        db.create_all()

        event = Event(title='Test Event', 
            date=date(2026, 8, 5), time=time(hour=10, minute=15, second=33))
        db.session.add(event)
        db.session.commit()

        saved_event = Event.query.first()

        assert saved_event is not None
        assert saved_event.title == 'Test Event'
        assert saved_event.date == date(2026, 8, 5)
        assert saved_event.time == time(hour=10, minute=15, second=33)

def test_long_event_name_persistence():
    """
    GIVEN a Event model
    WHEN a new Event is saved to the database
    THEN check the title is saved correctly
    """

    app = create_app(mode='test')

    with app.app_context():
        db.drop_all()
        db.create_all()

        event = Event(title='A very long event name', 
            date=date(2026, 8, 5), time=time(hour=10, minute=15, second=33))
        db.session.add(event)
        db.session.commit()

        saved_event = Event.query.first()

        assert saved_event is not None
        assert saved_event.title == 'A very long event name'
        assert saved_event.date == date(2026, 8, 5)
        assert saved_event.time == time(hour=10, minute=15, second=33)