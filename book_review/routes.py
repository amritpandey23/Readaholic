from book_review import app
from flask import render_template, url_for

@app.route("/")
@app.route("/catalog")
def home():
    return render_template("home.html")

