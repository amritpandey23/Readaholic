from book_review import app

@app.route("/")
def home():
    return "It works!"

