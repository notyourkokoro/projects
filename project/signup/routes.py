from flask import Blueprint, request, flash, redirect, render_template
from werkzeug.security import generate_password_hash
from string import ascii_uppercase, ascii_lowercase

from project.models import database, User
from flask_login import current_user

signup = Blueprint('signup', __name__)


def is_validate_password(password):
    if len(password) >= 8:
        flag_upper = False
        flag_lower = False
        flag_digit = False

        flag_another = False

        for char in password:
            if char.isdigit():
                flag_digit = True
            elif char in ascii_lowercase:
                flag_lower = True
            elif char in ascii_uppercase:
                flag_upper = True
            else:
                flag_another = True

        if flag_another:
            return False
        return flag_digit and flag_lower and flag_upper

    return False


def is_validate_username(username):
    if len(username) < 4:
        return False

    for char in username:
        if char not in ascii_uppercase and char not in ascii_lowercase:
            return False

    return True


@signup.route('/', methods=['POST', 'GET'])
def register_new_user():
    """Регистрация нового обычного пользователя"""

    if current_user.is_authenticated:
        return redirect('/profile')

    if request.method == 'POST':
        email = request.form['email']

        if is_validate_username(request.form['username']):
            username = request.form['username']
        else:
            flash('Invalid user name', 'error')
            return redirect('/signup')

        if is_validate_password(request.form['password']):
            password = generate_password_hash(request.form['password'])
        else:
            flash('The password must consist of eight or more characters and only Latin letters and digits', 'error')
            return redirect('/signup')

        try:
            if User.query.filter_by(email=email).first():
                flash('The user with this email is already registered', 'error')
            else:
                user = User(username=username, email=email, password_hash=password, status_id=1)
                database.session.add(user)
                database.session.commit()

                flash('Registration completed successfully!', 'success')

            return redirect('/signup')
        except Exception as e:
            return e

    else:
        return render_template('signup.html')