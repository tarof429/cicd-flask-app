import os, logging
from flask import Flask, render_template, request, flash, redirect, url_for, abort
from flask_migrate import Migrate
from sqlalchemy.exc import IntegrityError, DataError
from logging.handlers import RotatingFileHandler

from models import db, Event
from forms import *

import pika

def configure_logging():
    logs_dir = 'logs'

    os.makedirs(logs_dir, exist_ok = True)

    logsize = 10 * 10 * 1024 # 10MB
    handler = RotatingFileHandler(os.path.join(logs_dir, 'app.log'), 
                                       maxBytes = logsize, backupCount = 3)

    handler.setFormatter(logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    ))
    handler.setLevel(logging.INFO)

    return handler

def create_app(mode=None):
    app = Flask(__name__)

    file_handler = configure_logging()
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)

    if mode is None:
        mode = os.environ.get('RUNTIME_MODE', 'dev')

    if mode == 'test':
        app.config.from_object('config.TestConfig')
        app.config["WTF_CSRF_ENABLED"] = False
    elif mode == 'dev':
        app.config.from_object('config.DevConfig')
    elif mode == 'prod':
        app.config.from_object('config.ProdConfig')

    db.init_app(app)

    Migrate(app, db)

    @app.route('/')
    def index():
        app.logger.info("Home page accessed")

        return render_template('index.html')

    @app.route('/test')
    def test():
        return '<html><body>This is a test</body></html>'

    @app.route('/preferences',  methods=['GET', 'POST'])
    def preferences():
        form = PreferencesForm()

        if request.method == 'POST' and form.validate_on_submit():
            sysadminemail = form.sysadminemail.data
            notificationDelay = form.notificationDelay.data

            app.logger.info(f'Sysadmin email: {sysadminemail}')
            app.logger.info(f'Notification delay: {notificationDelay}')

            events = Event.query.all()
            return redirect(url_for('list_events', events = events))          

        return render_template('preferences.html', form=form, page_title = 'Preferences')

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
                if app.config['MESSAGE_BROKER_TYPE'] == 'rabbitmq':
                    app.logger.info(f'Publishing message for event: {new_event.title}')
                    publish_to_rabbitmq(f'Added new event: {new_event.title}!')
                    
                flash('Added event', 'success')
            except IntegrityError:
                db.session.rollback()
                app.logger.exception('Integrity error')
                flash('Event name must be unique', 'danger')
            except DataError:
                db.session.rollback()
                app.logger.exception('Invalid data submitted')
                flash('Invalid data submitted', 'danger')
            except Exception:
                db.session.rollback()
                app.logger.exception('Unhandled exception')
                flash('Error while creating event. Please contact administrator.', 'danger')

            events = Event.query.all()
            return render_template('events.html', events=events)

        return render_template('add_event_form.html', form=form, page_title='Add Event')

    @app.route('/update_event/<int:id>', methods=['GET', 'POST'])
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
                return redirect(url_for('list_events'))
            except IntegrityError:
                db.session.rollback()
                flash('Event name must be unique!', 'danger')
            except DataError:
                db.session.rollback()
                flash('Invalid data submitted', 'danger')
            except Exception as e:
                db.session.rollback()
                flash('An unhandled exception happened when calling update_event()', 'danger')
                flash(str(e), 'danger')

        return render_template('update_event_form.html', 
            form=form, page_title='Update event')
        
    @app.route('/delete_event/<int:id>')
    def delete_event(id):
        event = db.session.get(Event, id)
        if event is None:
            abort(404)

        db.session.delete(event)
        db.session.commit()
        
        flash('Event deleted', 'success')
        return redirect(url_for('list_events')) 

    return app

def publish_to_rabbitmq(message):
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
        channel.queue_declare(queue='event_confirmation', durable=True, arguments={'x-queue-type': 'quorum'})

        channel.basic_publish(exchange='',
                    routing_key='event_confirmation',
                    body=message)
    finally:
        if connection is not None:
            connection.close()