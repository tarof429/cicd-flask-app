import os, logging
from flask import Flask, render_template, request, flash, redirect, url_for, abort, Blueprint, current_app
from flask_migrate import Migrate
from sqlalchemy.exc import IntegrityError, DataError
from logging.handlers import RotatingFileHandler
import yaml
import pika
from .models import db, Event
from .forms import *
from .prefs import Prefs

events_bp = Blueprint('events', __name__)
    
@events_bp.route('/')
def index():
    current_app.logger.info("Home page accessed")

    return render_template('index.html')

@events_bp.route('/test')
def test():
    return '<html><body>This is a test</body></html>'

@events_bp.route('/preferences',  methods=['GET', 'POST'])
def preferences():
    prefs = Prefs(os.getenv('PREFERENCES_CONFIG', 'preferences.yaml'))

    form = PreferencesForm()

    if request.method == 'POST' and form.validate_on_submit():
        events = Event.query.all()

        if form.cancel.data:
            return redirect(url_for('events.list_events', events = events))
        else:
            fromEmail = form.fromEmail.data
            toEmail = form.toEmail.data
            notificationDelay = form.notificationDelay.data

            current_app.logger.info(f'From email: {fromEmail}')
            current_app.logger.info(f'To email: {toEmail}')
            current_app.logger.info(f'Notification delay: {notificationDelay}')

            data = {
                'from': fromEmail,
                'to': toEmail,
                'notificationDelay': notificationDelay
            }

            prefs.write(data)

            publish_to_rabbitmq('confirmation_prefs', 'confirmation_prefs', yaml.safe_dump(data))
            
            return redirect(url_for('events.list_events', events = events))

    data = prefs.load()

    current_app.logger.info(data)

    fromEmail = data.get("from")
    if fromEmail is None:
        form.fromEmail.data = ''
    else:
        form.fromEmail.data = fromEmail

    toEmail = data.get("to")
    if toEmail is None:
        form.toEmail.data = ''
    else:
        form.toEmail.data = toEmail


    notificationDelay = data.get('notificationDelay')
    if notificationDelay is None:
        form.notificationDelay.data = ''
    else:
        form.notificationDelay.data = notificationDelay

    return render_template('preferences.html', form = form, page_title = 'Preferences')

@events_bp.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

@events_bp.route('/list_events')
def list_events():
        events = Event.query.all()

        return render_template('events.html', events=events)

@events_bp.route('/event_action', methods=['POST'])
def event_action():

    event_id = request.form.get('event_id')
    action = request.form.get('action')

    if not event_id:
        flash('Please select an event', 'warning')
        return redirect(url_for('events.list_events'))
    
    if action == 'update':
        return redirect(url_for('events.update_event', id=event_id))
    elif action == 'delete':
        return redirect(url_for('events.delete_event', id=event_id))
    else:
        flash('Invalid action', 'danger')
        return redirect(url_for('events.list_events'))

@events_bp.route('/add_event', methods=['GET', 'POST'])
def add_event():
    form = AddEventForm()

    if request.method == 'POST' and form.validate_on_submit():
        new_event = Event(title=form.title.data, date=form.date.data, time=form.time.data)
        db.session.add(new_event)

        try:
            db.session.commit()
            if current_app.config['MESSAGE_BROKER_TYPE'] == 'rabbitmq':
                current_app.logger.info(f'Publishing message for event: {new_event.title}')
                publish_to_rabbitmq('event_confirmation', 
                                    'event_confirmation',  f'Added new event: {new_event.title}!')
                
            flash('Added event', 'success')
        except IntegrityError:
            db.session.rollback()
            current_app.logger.exception('Integrity error')
            flash('Event name must be unique', 'danger')
        except DataError:
            db.session.rollback()
            current_app.logger.exception('Invalid data submitted')
            flash('Invalid data submitted', 'danger')
        except Exception:
            db.session.rollback()
            current_app.logger.exception('Unhandled exception')
            flash('Error while creating event. Please contact administrator.', 'danger')

        events = Event.query.all()
        return render_template('events.html', events=events)

    return render_template('add_event_form.html', form=form, page_title='Add Event')

@events_bp.route('/update_event/<int:id>', methods=['GET', 'POST'])
def update_event(id):
    event = db.session.get(Event, id)
    if event is None:
        abort(404)
        
    form = UpdateEventForm(obj=event)

    if request.method == 'POST' and form.validate_on_submit():
        form.populate_obj(event)

        try:
            db.session.commit()
            flash('Event updated', 'success')
            return redirect(url_for('events.list_events'))
        except IntegrityError:
            db.session.rollback()
            flash('Event name must be unique!', 'danger')
        except DataError:
            db.session.rollback()
            flash('Invalid data submitted', 'danger')
        except Exception as e:
            db.session.rollback()
            flash('An unhandled exception hevents_bpened when calling update_event()', 'danger')
            flash(str(e), 'danger')

    return render_template('update_event_form.html', 
        form=form, page_title='Update event')
    
@events_bp.route('/delete_event/<int:id>')
def delete_event(id):
    event = db.session.get(Event, id)
    if event is None:
        abort(404)

    db.session.delete(event)
    db.session.commit()
    
    flash('Event deleted', 'success')
    return redirect(url_for('events.list_events')) 

def publish_to_rabbitmq(qname, rkey, message):
    credentials = pika.PlainCredentials(
        os.environ["RABBITMQ_USER"],
        os.environ["RABBITMQ_PASS"]
    )

    parameters = pika.ConnectionParameters(
        host = os.environ.get('RABBITMQ_HOST', 'rabbitmq'),
        virtual_host = os.environ.get('RABBITMQ_VHOST', "rabbitmq"),
        credentials = credentials
    )

    connection = None

    try:
        connection = pika.BlockingConnection(parameters)

        channel = connection.channel()
        channel.queue_declare(queue=qname, durable=True, arguments={'x-queue-type': 'quorum'})

        channel.basic_publish(exchange='',
                    routing_key=rkey,
                    body=message)
    finally:
        if connection is not None:
            connection.close()