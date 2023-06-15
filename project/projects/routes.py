from flask import Blueprint, render_template, request, redirect
from flask_login import login_required, current_user
from datetime import datetime

from project.models import database, Project, Task, UserInProject

projects = Blueprint('projects', __name__)


@projects.route('/')
@login_required
def show_projects():
    """Показать все созданные проекты в зависимости от статуса пользователя"""

    # администраторам доступен просмотр всех созданных проектов
    if current_user.status_id == 3:
        table_of_projects = Project.query.all()

    # лидеры и обычные пользователи могут просмотреть только те проекты, в которых участвуют
    else:
        table_of_projects = [el.project for el in current_user.projects]

    return render_template('projects.html', table_of_projects=table_of_projects, current_user=current_user)


@projects.route('/create-project', methods=['POST', 'GET'])
@login_required
def create_project():
    """Создание нового проекта лидером"""

    if current_user.status_id == 2:
        if request.method == 'POST':
            title = request.form['title']
            description = request.form['description']

            if request.form['created_date']:
                created_date = request.form['created_date']
            else:
                created_date = datetime.now()

            status = request.form['status']

            project = Project(title=title, description=description, created_date=created_date, owner_id=current_user.id, status=status)

            try:
                database.session.add(project)
                database.session.commit()

                user_in_project = UserInProject(user_id=current_user.id, project_id=project.id)
                database.session.add(user_in_project)
                database.session.commit()

                return redirect('/projects')
            except Exception as e:
                return e

        return render_template('create-project.html')

    return redirect('/profile')


@projects.route('/<int:project_id>', methods=['GET', 'POST'])
@login_required
def project_detail(project_id):
    """Просмотр конкретного проекта"""

    project = Project.query.get_or_404(project_id)
    user_id = current_user.id
    status_id = current_user.status_id

    user_flag = project_id in [el.project_id for el in current_user.projects]

    # администраторы и лидеры проекта могут просматривать все задачи в нем
    if status_id == 3 or (status_id == 2 and user_flag):
        if request.method == 'POST':
            title = request.form['title']
            description = request.form['description']
            user_id = request.form['user_id']

            task = Task(title=title, description=description, created_date=datetime.now(), project_id=project_id,
                        owner_id=current_user.id, user_id=user_id, status='not completed', approve=1)
            database.session.add(task)
            database.session.commit()

            return redirect(f'/projects/{project_id}')
        return render_template('/project-detail.html', project=project, status_id=status_id, user_id=user_id)

    # обычный пользователь может просматривать только свои задачи
    else:
        if user_flag:
            return render_template('/project-detail.html', project=project, status_id=status_id, user_id=user_id)
        return redirect('/no-access')


@projects.route('/<int:project_id>/del')
@login_required
def project_delete(project_id):
    """Удаление проекта лидером с каскадным удалением всех задач и связей между проектом и пользователем"""

    project = Project.query.get_or_404(project_id)

    if current_user.id == project.owner_id:
        try:
            database.session.delete(project)
            database.session.commit()
            return redirect('/projects')
        except Exception as e:
            return e

    return redirect('/no-access')


@projects.route('/<int:project_id>/update', methods=['POST', 'GET'])
@login_required
def project_update(project_id):
    """Внесение изменений в проект лидером"""

    project = Project.query.get_or_404(project_id)
    if current_user.id == project.owner_id:

        if request.method == 'POST':
            project.title = request.form['title']
            project.description = request.form['description']
            project.status = request.form['status']

            try:
                database.session.commit()
                return redirect(f'/projects/{project_id}')
            except Exception as e:
                return e

        return render_template('project-update.html', project=project)
    return redirect('/no-access')


@projects.route('<int:project_id>/<int:task_id>/del')
@login_required
def task_delete(project_id, task_id):
    """Удаление задачи лидером"""

    task = Task.query.get_or_404(task_id)
    if current_user.status_id == 2 and project_id in [el.project_id for el in current_user.projects]:

        try:
            database.session.delete(task)
            database.session.commit()
            return redirect(f'/projects/{project_id}')
        except Exception as e:
            return e

    return redirect('/no-access')


@projects.route('<int:project_id>/<int:task_id>/update')
@login_required
def task_update(project_id, task_id):
    """Изменение статуса задачи обычным пользователем"""

    task = Task.query.get_or_404(task_id)

    if current_user.id == task.user_id:
        task.status = 'in progress' if task.status == 'not completed' else 'completed'
        task.approve = 0

        try:
            database.session.commit()
            return redirect(f'/projects/{project_id}')
        except Exception as e:
            return e

    return redirect('/no-access')


@projects.route('<int:project_id>/<int:task_id>/approve')
@login_required
def task_approve(project_id, task_id):
    """Подтверждение статуса задачи ее создателем"""

    task = Task.query.get_or_404(task_id)

    if current_user.status_id == 2 and project_id in [el.project_id for el in current_user.projects]:
        task.approve = 1

        try:
            database.session.commit()
            return redirect(f'/projects/{project_id}')
        except Exception as e:
            return e

    return redirect('/no-access')