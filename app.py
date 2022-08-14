# from crypt import methods
# from email import message
from flask import Flask, request, render_template, jsonify, session

app = Flask(__name__)

app.secret_key = 'secretkey'

books = [
    {
        "author": "Hernando de Soto",
        "country": "Peru",
        "language": "English",
        "pages": 209,
        "title": "The Myster of Captial",
        "year": 1970

    },
    {
        "author": "Hans Christian Andersen",
        "country": "Denmark",
        "language": "Danish",
        "pages": 784,
        "title": "Fairy Tales",
        "year": 1836

    },
    {
        "author": "Dante Alighieri",
        "country": "Italy",
        "language": "Italian",
        "pages": 928,
        "title": "The Divine Comedy",
        "year": 1315

    }
]

# _username = 'Faateh'

users = [
    {
        "username": "testuser",
        "password": "testuser"
    }
]

def checkuser(username, password):
    for user in users:
        if username in user["username"] and password in user["password"]:
            return True
    return False


# @app.route("/", methods=["GET"]) --old
# def index():
#     return render_template('index.html', username=_username)

@app.route("/", methods=["GET"])
def home():
    return render_template('register.html')


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if checkuser(username, password):
            session["username"] = username
            return render_template('index.html', username = session["username"])
        else:
            return render_template('register.html')
    
    elif request.method =="GET":
        return render_template('register.html')

@app.route("/logout")
def logout():
     # remove the username from the session if it is there
    session.pop("username", None)
    return "Logged Out of Books"

@app.route("/books", methods=["GET"])
def get_books():
    return render_template('books.html', books = books, username = session["username"])

if __name__ == '__main__':
    app.run(debug=True)
