from flask import Blueprint, render_template
from flask_login import current_user

main = Blueprint('main', __name__)


@main.route('/')
def index():
    """Загрузка начальной страницы"""

    try:
        current_user.id
        return render_template('index-login.html')
    except:
        return render_template('index-logout.html')


@main.route('/no-access')
def no_access():
    """Загрузка страницы, которая указывает на отсутствие доступа"""

    return render_template('no-access.html')