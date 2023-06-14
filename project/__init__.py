from flask import Flask

from project.main.routes import main
from project.signup.routes import signup
from project.login.routes import login
from project.projects.routes import projects
from project.profile.routes import profile

from project.config import DevelopmentConfig
from project.models import database, login_manager


app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

database.init_app(app)

login_manager.init_app(app)
login_manager.login_view = '/login'
login_manager.login_message = 'Please log in to access this page'


app.register_blueprint(main, url_prefix='/')
app.register_blueprint(signup, url_prefix='/signup')
app.register_blueprint(login, url_prefix='/login')
app.register_blueprint(projects, url_prefix='/projects')
app.register_blueprint(profile, url_prefix='/profile')
