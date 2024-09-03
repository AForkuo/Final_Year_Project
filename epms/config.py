import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    WTF_CSRF_ENABLED = True

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/epms_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = os.path.join(basedir, 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB limit
    ALLOWED_EXTENSIONS = {'.pdf', '.doc', '.docx', '.txt'}
    

    MAIL_SERVER='live.smtp.mailtrap.io'
    MAIL_PORT = 587
    MAIL_USERNAME = 'api'
    MAIL_PASSWORD = '7a1b87f33570d746d78b533a11a53372'
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
