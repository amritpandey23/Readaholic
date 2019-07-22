from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json

# parse config data
with open("book_review/config.json") as f:
    data = json.load(f)

app = Flask(__name__)
# app config
app.config["SECRET"] = data["app_secret"],
app.config["SQLALCHEMY_DATABASE_URI"] = data["sqlalchemy_database_uri"]

# database
db = SQLAlchemy(app)

# routes
from book_review import routes


