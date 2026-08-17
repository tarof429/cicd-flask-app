from flask import Flask, render_template, request, flash
from flask_migrate import Migrate
from sqlalchemy.exc import IntegrityError, DataError

from models import db, Event
from forms import AddEventForm

app = Flask(__name__)
app.config.from_pyfile('config.py')
db.init_app(app)

Migrate(app, db)

@app.route('/')
def index():
    return render_template('index.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

@app.route('/list_events')
def list_events():
        events = Event.query.all()

        return render_template('events.html', events=events)

@app.route('/add_event', methods=['GET', 'POST'])
def add_event():
    form = AddEventForm()

    if request.method == 'POST' and form.validate_on_submit():
        new_event = Event(title=form.title.data, date=form.date.data, time=form.time.data)
        db.session.add(new_event)

        try:
            db.session.commit()
            flash('Added event', 'success')
        except IntegrityError:
            flash('Event name must be unique', 'danger')
            db.session.rollback()
        except DataError:
            flash('Invalid data submitted', 'danger')
            db.session.rollback()
        except Exception as e:
            flash(str(e), 'danger')
            db.session.rollback()

        events = Event.query.all()
        return render_template('events.html', events=events)

    return render_template('add_event_form.html', form=form, page_title='Add Event')

if __name__ == '__main__':
    app.run()