import app

import os
from app import publish_to_rabbitmq

def test_publish_to_rabbitmq(app):
    with app.app_context():
        os.environ["RABBITMQ_USER"] = 'user'
        os.environ["RABBITMQ_PASS"] = 'password'
        publish_to_rabbitmq('event_confirmation', 'event_confirmation', 'test message')

