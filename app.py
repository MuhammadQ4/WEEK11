from re import M
from flask import Flask, request, render_template, session
from flask import redirect
from functools import wraps
import os
import json

app = Flask(__name__)
app.secret_key = "secretkey"
app.config["UPLOADED_PHOTOS_DEST"] = "static"

### end swagger specific ###
books = [
    {
        "author": "Hernando de Soto",
        "country": "Peru",
        "language": "English",
        "pages": 209,
        "title": "The Mystery of Capital",
        "year": 1970,
    },
    {
        "author": "Hans Christian Andersen",
        "country": "Denmark",
        "language": "Danish",
        "pages": 784,
        "title": "Fairy tales",
        "year": 1836,
    },
    {
        "author": "Dante Alighieri",
        "country": "Italy",
        "language": "Italian",
        "pages": 928,
        "title": "The Divine Comedy",
        "year": 1315,
    },
]

users = [
            {"username": "testuser", "password": "testuser"},
            {"username": "Faateh", "password": "Faateh"}
         ]

def sessionRequired(fn):
    @wraps(fn)
    def decorator(*args, **kwargs):
        frombrowser = session["username"]
        for user in users:
            if session["username"] in frombrowser:
                    return fn(*args, **kwargs)

        return redirect("templates/register.html")

    return decorator

@app.route("/", methods=["GET"])
def firstRoute():
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = {"username":request.form["username"], "password": request.form["password"]}

        if user in users:
            # set session data
            session["username"] =  request.form["username"]
            return render_template(
                "index.html", username=session["username"], title = 'books', books = books)
        else:
            return render_template("register.html")
    else:
        return render_template("register.html")


@app.route("/logout")
def logout():
    # remove the username from the session if it is there
    session.pop("username", None)
    return "You are successfully logged out!"


@app.route("/books", methods=["GET"])
@sessionRequired
def book():
    username = session["username"]
    return render_template(
            "books.html", books=books, username=username, title="books"
        )


@app.route("/addbook", methods=["GET", "POST"])
@sessionRequired
def addBook():
    username = session["username"]
    if request.method == "GET":
        return render_template("addBook.html")
    if request.method == "POST":
        # expects pure json with quotes everywheree
        new_book = request.form["book"]
        myjson = json.loads(new_book)
        books.append(myjson)
        return render_template(
            "books.html", books=books, username=username, title="books"
        )
    else:
        return 400

if __name__ == "__main__":
    app.run(debug=True)
    # app.run(debug=True, host="0.0.0.0", port=5000)
