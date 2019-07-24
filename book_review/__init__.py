from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import json

# parse config data
with open("book_review/config.json") as f:
    data = json.load(f)

app = Flask(__name__)
# app config
app.config["SECRET_KEY"] = data["app_secret"]
app.config["SQLALCHEMY_DATABASE_URI"] = data["sqlalchemy_database_uri"]

# bcrypt initialisation
bcrypt = Bcrypt(app)

# database
db = SQLAlchemy(app)

#login manager
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"

# routes
from book_review import routes


