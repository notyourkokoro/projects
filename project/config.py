# import os
#
# BASE_DIR = os.path.abspath(os.path.dirname(__name__))


class BaseConfig:
    DEBUG = False
    TESTING = False

    SECRET_KEY = '07a45843e1fe9896f99c5b4e84eeb63cf59ee2bd'

    # MySQL
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://dilstey:97Pl8S-vElJhE@localhost/note'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = True
