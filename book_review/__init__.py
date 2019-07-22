from flask import Flask

app = Flask(__name__)
app.config["SECRET"] = "3c794f0c67bd561ce841fc6a5999bf0df298a0f0ae3487efda9d0ef4"

from book_review import routes


