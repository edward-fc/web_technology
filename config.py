import os

# Enable the Flask-WTF cross site request forgery (CSRF) prevention
WTF_CSRF_ENABLED = True
SECRET_KEY = 'a-very-secret-secret'

# Define the database
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'spam_call_reporter.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
