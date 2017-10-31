import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'ruhvejri392wef'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    SQLALCHEMY_BINDS = {
        "users" : 'sqlite:///' + os.path.join(basedir, 'user.sqlite')
    }
    DEBUG = True

    @staticmethod
    def init_app(app):
        pass
