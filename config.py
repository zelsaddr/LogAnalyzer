import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'my-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mysql://root:@localhost/loganalyzer'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TEMPLATES_AUTO_RELOAD = True
    DEBUG = True
    TESTING = True
    UPLOAD_PATH = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), 'uploads')
    TIMEOUT = 60
