from flask import Blueprint, request, flash, redirect, render_template
from werkzeug.security import generate_password_hash

from project.models import database, User
from flask_login import current_user

signup = Blueprint('signup', __name__)


@signup.route('/', methods=['POST', 'GET'])
def register_new_user():
    """Регистрация нового обычного пользователя"""

    if current_user.is_authenticated:
        return redirect('/profile')

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])

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