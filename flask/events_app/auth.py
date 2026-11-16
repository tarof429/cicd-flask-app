from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .forms import LoginForm, RegisterForm, ProfileForm
from .models import Event, User
from . import db

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

        login_user(user)
        return redirect(url_for('events.index'))

    return render_template('login_form.html', form=form, page_title='Login')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if request.method == 'POST':
        if form.cancel.data:
            return redirect(url_for('events.index'))
        elif form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            name = form.name.data

            user = User.query.filter_by(username=username).first()

            if user:
                flash('User already registered.', 'danger')
                return redirect(url_for('auth.register'))
            new_user = User(username = username, 
                             password = generate_password_hash(password),
                             name = name)

            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('auth.login'))

    return render_template('register_form.html', form=form, page_title='Signup')

@auth.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm()

    form.username.data = current_user.username
    form.name.data = current_user.name

    if request.method == 'POST':
        if form.cancel.data:
            return redirect(url_for('envents.index'))
        elif form.validate_on_submit():
            username = form.username.data
            newPassword = form.newPassword.data
            newPasswordAgain = form.newPasswordAgain.data
            name = form.name.data

            user = User.query.filter_by(username=username).first()

            if user:
                if newPassword != newPasswordAgain:
                    flash('Passwords do not match', 'warning')
                else:
                    user.password = newPassword
                    user.name = name
                    db.session.commit()

                    return redirect(url_for('events.index'))

    return render_template('profile_form.html', form=form, page_title='Profile')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('events.index'))