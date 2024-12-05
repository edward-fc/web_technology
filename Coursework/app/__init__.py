from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect


# Create a Flask app
app = Flask(__name__)
csrf = CSRFProtect(app)
app.config.from_object('config')

# Create a SQLAlchemy object
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import views, models
