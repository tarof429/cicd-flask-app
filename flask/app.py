from flask import Flask, render_template, request, flash
from flask_migrate import Migrate

from models import db
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
    return render_template('events.html')

@app.route('/add_event', methods=['GET', 'POST'])
def add_event():
    form = AddEventForm()

    if request.method == 'POST' and form.validate_on_submit():
        flash('Added event', 'success')

    return render_template('add_event_form.html', form=form, page_title='Add Event')

if __name__ == '__main__':
    app.run()