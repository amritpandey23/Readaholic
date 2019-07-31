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
from book_review.book.routes import book
from book_review.admins.routes import admins
from book_review.main.routes import main
from book_review.errors.handlers import errors

app.register_blueprint(book)
app.register_blueprint(admins)
app.register_blueprint(main)
app.register_blueprint(errors)