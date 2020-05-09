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
        return redirect(url_for("search"))
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
        return redirect(url_for("login"))
    else:
        # TODO this is actually maybe not quiiiiite how it's supposed to work oops fix???
        return render_template("signup.html", name="Signup", message="User already exists!")

@app.route("/results/")
def results():
    # If not logged in, display a message directing you to login
    if 'user' not in session.keys():
        return render_template("results.html", name="Book", logged_in=False)

    mode = request.args.get('query_type')
    query_string = request.args.get('query')

    if mode not in ['isbn', 'author', 'title']:
        return render_template("results.html", name="Book", error=True, logged_in=True)
    
    books = dao.get_books(mode, query_string)
    print(books)
    
    return render_template("results.html", name="Book", logged_in=True, books=books)

@app.route("/book/<isbn>")
def book(isbn):
    book_info = bookapi.query(isbn)
    if not book_info:
        return render_template("book.html", error=True)
    reviews_count = book_info['reviews_count']
    average_rating = book_info['average_rating']

    book = dao.get_books('isbn', isbn, strict=True)
    if len(book) < 1:
        return render_template("book.html", error=True)
    book = book[0]
    title = book['title']
    author = book['author']
    year = book['year']
    reviews = dao.get_reviews(isbn)
    
    return render_template("book.html", name='Book', title=title, isbn=isbn, author=author, 
        year=year, reviews_count=reviews_count, average_rating=average_rating, reviews=reviews)
    

@app.route("/search/")
def search():
    return render_template("search.html")

@app.route("/submit_review/", methods=['POST'])
def submit_review():
    username = session['user']
    rating = request.form.get('rating')
    review_content = request.form.get('review_content')
    isbn = request.form.get('isbn')
    dao.add_review(username, rating, review_content, isbn)
    return redirect(url_for("book", isbn=isbn))

@app.route("/api/<isbn>")
def api(isbn):
    try:
        basic_info = dao.get_books('isbn', isbn)[0]

        book_info = bookapi.query(isbn)

        resp = {
            'isbn':   basic_info['isbn'],
            'title':  basic_info['title'],
            'author': basic_info['author'],
            'year':   basic_info['year'],
            'review_count': book_info['reviews_count'],
            'average_score': book_info['average_rating']
        }
        return resp
    except Exception:
        return "404 error!", 404
