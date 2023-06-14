from flask_sqlalchemy import SQLAlchemy
from flask_login import (LoginManager, UserMixin)
from werkzeug.security import generate_password_hash, check_password_hash

database = SQLAlchemy()
login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(database.Model, UserMixin):
    __tablename__ = 'users'

    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(50), unique=True, nullable=False)
    email = database.Column(database.String(320), unique=True, nullable=False)
    password_hash = database.Column(database.String(255), nullable=False)
    status_id = database.Column(database.Integer, nullable=False)

    projects = database.relationship('UserInProject', backref='user', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.id

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Project(database.Model):
    __tablename__ = 'projects'

    id = database.Column(database.Integer, primary_key=True)
    title = database.Column(database.String(255), nullable=False)
    description = database.Column(database.Text)
    created_date = database.Column(database.DateTime, nullable=False)
    last_modified_date = database.Column(database.TIMESTAMP,
                                         nullable=False,
                                         server_default=database.func.current_timestamp(),
                                         onupdate=database.func.current_timestamp())
    owner_id = database.Column(database.Integer, nullable=False)
    status = database.Column(database.Enum('active', 'frozen', 'rejected', 'completed'), nullable=False)

    tasks = database.relationship('Task', backref='project', cascade='all, delete-orphan', lazy=True)
    users_in_projects = database.relationship('UserInProject', backref='project', cascade='all, delete-orphan', lazy=True)

    def __repr__(self):
        return '<Project %r>' % self.id


class Task(database.Model):
    __tablename__ = 'tasks'

    id = database.Column(database.Integer, primary_key=True)
    title = database.Column(database.String(255), nullable=False)
    description = database.Column(database.Text)
    created_date = database.Column(database.DateTime, nullable=False)
    last_modified_date = database.Column(database.TIMESTAMP,
                                         nullable=False,
                                         server_default=database.func.current_timestamp(),
                                         onupdate=database.func.current_timestamp())
    project_id = database.Column(database.Integer,
                                 database.ForeignKey('projects.id', ondelete='CASCADE'),
                                 nullable=False)
    owner_id = database.Column(database.Integer, nullable=False)
    user_id = database.Column(database.Integer, database.ForeignKey('users.id'), nullable=False)
    status = database.Column(database.Enum('not completed', 'in progress', 'completed'), nullable=False)
    approve = database.Column(database.Integer, nullable=False)

    def __repr__(self):
        return '<Task %r>' % self.id


class UserInProject(database.Model):
    __tablename__ = 'users_in_projects'

    id = database.Column(database.Integer, primary_key=True)
    user_id = database.Column(database.Integer, database.ForeignKey('users.id'), nullable=False)
    project_id = database.Column(database.Integer, database.ForeignKey('projects.id'), nullable=False)
