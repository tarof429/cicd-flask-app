from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user
from werkzeug.security import generate_password_hash, check_password_hash
from .forms import LoginForm
from .models import User

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()

        if not user or not check_password_hash(user.password, password):
            flash('Please check your login details and try again.', 'danger')
            return redirect(url_for('auth.login'))

        # login_user(user)
        return redirect(url_for('events.list_events'))

    return render_template('login_form.html', form=form, page_title='Login')