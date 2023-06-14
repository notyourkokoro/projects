from flask import Blueprint, render_template, redirect, request, flash
from flask_login import current_user, login_required

from project.models import database, User, UserInProject

profile = Blueprint('profile', __name__)


@profile.route('/', methods=['GET', 'POST'])
@login_required
def user_profile():
    """Загрузка профиля пользователя в зависимости от его статуса"""

    status = {1: 'User', 2: 'Leader', 3: 'Admin'}[current_user.status_id]
    table_of_projects = [el.project for el in current_user.projects]

    if request.method == 'POST':
        user_id = request.form['user_id']
        user = User.query.get(user_id)

        if user:
            project_id = int(request.form['project_id'])
            projects = [el.project_id for el in user.projects]

            if project_id not in projects:
                user_in_project = UserInProject(user_id=user_id, project_id=project_id)
                try:
                    database.session.add(user_in_project)
                    database.session.commit()

                    flash('The user has been successfully added to the project!', 'success')
                except Exception as e:
                    return e
            else:
                flash('The user is already involved in this project!', 'error')
        else:
            flash('There is no user with this ID!', 'error')

    return render_template('profile.html', current_user=current_user, status=status, table_of_projects=table_of_projects)


@profile.route('/update')
@login_required
def update_profile():
    """Обновление профиля пользователя до статуса Leader"""

    user = User.query.get_or_404(current_user.id)
    user.status_id = 2

    try:
        database.session.commit()
        return redirect('/profile')
    except Exception as e:
        return e