from flask import Flask, render_template, request, flash, redirect, url_for
from flask_migrate import Migrate
from sqlalchemy.exc import IntegrityError, DataError

from models import db, Event
from forms import AddEventForm, UpdateEventForm

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

@app.route('/event_action', methods=['POST'])
def event_action():

    event_id = request.form.get('event_id')
    action = request.form.get('action')

    if not event_id:
        flash('Please select an event', 'warning')
        return redirect(url_for('list_events'))
    
    if action == 'update':
        return redirect(url_for('update_event', id=event_id))
    elif action == 'delete':
        return redirect(url_for('delete_event', id=event_id))
    else:
        flash('Invalid action', 'danger')
        return redirect(url_for('list_events'))

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

@app.route('/update_event/<int:id>', methods=['GET', 'POST'])
def update_event(id):
    event = Event.query.get_or_404(id)

    form = UpdateEventForm(obj=event)

    if request.method == 'POST' and form.validate_on_submit():
        form.populate_obj(event)

        try:
            db.session.commit()
            flash('Event updated', 'success')
            return redirect(url_for('list_events'))
        except IntegrityError:
            flash('Event name must be unique!', 'danger')
            db.session.rollback()
        except DataError:
            flash('Invalid data submitted', 'danger')
            db.session.rollback()
        except Exception as e:
            flash('An unhandled exception happened when calling update_event()', 'danger')
            flash(str(e), 'danger')
            db.session.rollback()
    
    return render_template('update_event_form.html', 
        form=form, page_title='Update event')
    
@app.route('/delete_event/<int:id>')
def delete_event(id):
    event = Event.query.get_or_404(id)
    db.session.delete(event)
    db.session.commit()
    
    flash('Event deleted', 'success')
    return redirect(url_for('list_events')) 

    return app

if __name__ == '__main__':
    app.run()