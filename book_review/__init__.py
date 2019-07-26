import json
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_pagedown import PageDown

# parse config data
with open("book_review/config.json") as f:
    _config = json.load(f)

app = Flask(__name__)
# app config
app.config["SECRET_KEY"] = _config["app_secret"]
app.config["SQLALCHEMY_DATABASE_URI"] = _config["sqlalchemy_database_uri"]

# bcrypt initialisation
bcrypt = Bcrypt(app)

# database
db = SQLAlchemy(app)

# markdown editor
pagedown = PageDown(app)

# login manager
login_manager = LoginManager(app)
login_manager.login_view = _config["login_view"]
login_manager.login_message_category = "info"

# routes
from book_review import routes

