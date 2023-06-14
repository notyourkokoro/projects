from flask import Blueprint, render_template, flash, redirect
from flask_login import login_user, current_user, logout_user, login_required

from project.forms import LoginForm
from project.models import User

login = Blueprint('login', __name__)


@login.route('/', methods=['POST', 'GET'])
def login_page():
    """Вход пользователя в аккаунт по email"""

    if current_user.is_authenticated:
        return redirect('/projects')

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect('/projects')

        flash('Please check your login details and try again')
        return redirect('/login')

    return render_template('login.html', form=form)


@login.route('/logout')
@login_required
def logout():
    """Выхода пользователя из аккаунта"""

    logout_user()
    flash('You have been logged out')
    return redirect('/login')