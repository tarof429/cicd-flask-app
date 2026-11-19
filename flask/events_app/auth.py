from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import click
from .forms import LoginForm, RegisterForm, ProfileForm
from .models import User
from . import db
from .models import User
from . import USER_ROLE, ADMIN_ROLE

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data.strip()
        password = form.password.data.strip()

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
            username = form.username.data.strip()
            password = form.password.data.strip()
            name = form.name.data.strip()

            user = User.query.filter_by(username=username).first()

            if user:
                flash('User already registered.', 'danger')
                return redirect(url_for('auth.register'))

            new_user = User(username = username, 
                             password = generate_password_hash(password),
                             name = name,
                             role = USER_ROLE)

            db.session.add(new_user)
            db.session.commit()
            flash('Successfully registered.', 'success')
            return redirect(url_for('auth.login'))

    return render_template('register_form.html', form=form, page_title='Signup')

@auth.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm()

    if request.method == 'GET':
        form.username.data = current_user.username
        form.name.data = current_user.name
    elif request.method == 'POST':
        if form.cancel.data:
            return redirect(url_for('events.index'))
        
        if form.validate_on_submit():
            current_user.name = form.name.data.strip()
        
            rules = [
               form.newPassword.data.strip() != '',
               form.newPasswordAgain.data.strip() != '',
               form.newPassword.data.strip() == form.newPasswordAgain.data.strip()
            ]

            if all(rules):
                current_user.password = generate_password_hash(form.newPassword.data.strip())
            
            try:
                db.session.commit()
                flash('Profile updated.', 'success')
            except Exception as e:
                db.session.rollback()
                flash('An unhandled exception hevents_bpened when updating profile', 'danger')
                flash(str(e), 'danger')

            return redirect(url_for('auth.profile'))

    return render_template('profile_form.html', form=form, page_title='Profile')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('events.index'))

@auth.cli.command('create')
@click.password_option('--pswd', default='admin', help='Password for admin users')
def create_admin_user(pswd = 'admin'):
    create(pswd)

def create(pswd = 'admin'):
    user = User.query.filter_by(username='admin').first()

    if user:
        click.echo('admin user already exists')
    if not user:
        click.echo('Creating admin user')              
        new_user = User(username = 'admin', 
            password = generate_password_hash(pswd),
            name = 'admin',
            role = ADMIN_ROLE)

        db.session.add(new_user)
        db.session.commit()