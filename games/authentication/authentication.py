from flask import Blueprint, render_template, redirect, url_for, session

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, ValidationError, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

from password_validator import PasswordValidator

from functools import wraps

import games.adapters.repository as repo
import games.authentication.services as services

authentication_blueprint = Blueprint('auth_bp', __name__, url_prefix='/authentication')

class PasswordValid(): # I feel like a lot of this stuff should be in services, but It's here in the covid app, so I guess this is where it should be.
    def __init__(self, message=None):
        if not message:
            message = 'Password must be at least 8 characters long, contain at least one uppercase letter, one lowercase letter, and one digit.'
        self.message = message
    
    def __call__(self, form, field):
        schema = PasswordValidator()
        schema\
            .min(8)\
            .has().uppercase()\
            .has().lowercase()\
            .has().digits()
        if not schema.validate(field.data):
            raise ValidationError(self.message)

class RegistrationForm(FlaskForm):
    username = StringField('Username', [
        DataRequired(message='Username required'),
        Length(min=3, message='Username must be at least 3 characters long')
        ])
    password = PasswordField('Password', [
        DataRequired(message='Password required'),
        PasswordValid()
        ])
    submit = SubmitField('Sign Up!')

class LoginForm(FlaskForm):
    username = StringField('Username', [
        DataRequired(message='Username required'),
    ])
    password = PasswordField('Password', [
        DataRequired(message='Password required'),
    ])
    submit = SubmitField('Log In!')

@authentication_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    
    if form.validate_on_submit():
        try:
            services.add_user(form.username.data, form.password.data, repo.repo_instance)
            # If successful redirect to login.
            # Should add a little greed box saying registration successful.
            return redirect(url_for('auth_bp.login'))
        except services.NameNotUniqueException:
            form.username.errors.append('Username taken')

    # If not successful, or first time visiting page, render page.
    return render_template(
        'authenticate.html',
        title='Sign up',
        form=form,
        form_url=url_for('auth_bp.register')
    )

@authentication_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        try:
            services.authenticate_user(form.username.data, form.password.data, repo.repo_instance)
            session.clear()
            session['username'] = form.username.data
            return redirect(url_for('profile_bp.profile'))
        except services.UnknownUserException:
            form.username.errors.append('Unknown username')
        except services.AuthenticationException:
            form.password.errors.append('Incorrect password')

    # If not successful, or first time visiting page, render page.
    return render_template(
        'authenticate.html',
        title='Log in',
        form=form,
        form_url=url_for('auth_bp.login')
    )

@authentication_blueprint.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))


def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if session.get('username') is None:
            return redirect(url_for('auth_bp.login'))
        return view(**kwargs)
    return wrapped_view
