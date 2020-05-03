import os
import csv

from flask import Flask, session, render_template, request, redirect, url_for
from flask_session import Session
from API.DAO import DAO

import API.bookapi as bookapi

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Move to initialize function??
dao = DAO()
print(dao.get_users())
#session['login_error'] = False

base = "base.html"

@app.route("/")
def index():
    return render_template(base, name="Home")

@app.route("/register/")
def register():
    return render_template(base, name="Register")

@app.route("/login/")
def login():
    return render_template("login.html", name="Login", error=False, logged_in=('user' in session.keys() and session['user']))

@app.route("/login_user/", methods=["POST"])
def login_user():
    username = request.form.get("username")
    password = request.form.get("password")
    if dao.matches(username, password):
        session['user'] = username
        return redirect(url_for("book"))
    else:
        return render_template("login.html", name="Login", error=True)

@app.route("/logout/")
def logout():
    session.pop('user', None)
    return render_template("logout.html")

@app.route("/signup/")
def signup():
    return render_template("signup.html", name="Signup")

@app.route("/signup_user/", methods=["POST"])
def signup_user():
    username = request.form.get("username")
    password = request.form.get("password")
    if dao.try_create_user(username, password):
        session['user'] = username
        print("SESSION USER: ", session['user'])
        return redirect(url_for("book"))
    else:
        # TODO this is actually maybe not quiiiiite how it's supposed to work oops fix???
        return render_template("signup.html", name="Signup", message="User already exists!")

@app.route("/book/")
def book():
    if 'user' not in session.keys():
        return render_template("book_home.html", name="Book", logged_in=False)
    return render_template("book_home.html", name="Book", username=session['user'], logged_in=True)


@app.route("/api/<isbn>")
def api(isbn):
    basic_info = dao.get_bookinfo(isbn)
    if basic_info is None:
        return "404 error!", 404

    book_info = bookapi.query(isbn)['books'][0]
    resp = {
        'isbn':   basic_info.isbn,
        'title':  basic_info.title,
        'author': basic_info.author,
        'year':   basic_info.year,
        'review_count': book_info['reviews_count'],
        'average_score': book_info['average_rating']
    }
    return resp