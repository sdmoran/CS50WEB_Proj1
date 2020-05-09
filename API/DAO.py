import os
import csv
import string
import random
import hashlib

from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker

class DAO:
    def __init__(self):
        self.engine = create_engine(os.getenv("DATABASE_URL"))
        self.db = scoped_session(sessionmaker(bind=self.engine))

    def add_user(self, username, password):
        # Hash password
        salt = username
        password_hash = self.get_hash(password, salt)
        query = text("INSERT INTO users(username, password_hash) VALUES(:username, :password_hash);")

        print("USERNAME: ", username)
        print("HASH: ", password_hash)
        self.db.execute(query, {'username': username, 'password_hash': password_hash})
        self.db.commit()

    def get_hash(self, password, salt):
        m = hashlib.sha256()
        m.update(bytes(password, 'utf-8'))
        m.update(bytes(salt, 'utf-8'))
        print(str(m.digest()))
        return str(m.digest())

    def get_users(self):
        resultproxy = self.db.execute("SELECT id, username FROM users;")
        result = []

        for row in resultproxy:
            result.append(row)

        return result

    def try_create_user(self, username, password):
        if not self.user_exists(username):
            self.add_user(username, password)
            return True
        else:
            return False

    def user_exists(self, username):
        query = text("SELECT COUNT(username) FROM users WHERE username=:username;")
        result = self.db.execute(query, {'username': username})

        count = result.first()[0]

        if count == 0:
            return False
        else:
            return True

    def matches(self, username, password):
        query = text("SELECT password_hash FROM users WHERE username=:username;")
        result = self.db.execute(query, {'username': username}).first()
        if result is None:
            return False
        stored_password = result[0]
        print("STORED: ", stored_password)
        print("PROVIDED: ", password)
        return stored_password == self.get_hash(password, username)

    def get_books(self, mode, query_string, strict=False):
        query = f"SELECT isbn, title, author, year FROM books WHERE {mode} ~ :query_string;"
        if mode not in ['isbn', 'author', 'title']:
            return []
        if strict:
            query = f"SELECT isbn, title, author, year FROM books WHERE {mode} = :query_string;"
        query = text(query)
        response = self.db.execute(query, {'mode': mode, 'query_string': query_string})
        result = [{'isbn': row['isbn'], 'title': row['title'], 'author': row['author'], 'year': row['year']} for row in response ]
        return result

    def get_reviews(self, isbn):
        query = text("SELECT username, rating, review_content FROM reviews WHERE isbn=:isbn;")
        response = self.db.execute(query, {'isbn': isbn})
        result = [{'username': row['username'], 'rating': row['rating'], 'content': row['review_content']} for row in response]
        return result

    def add_review(self, username, rating, review_content, isbn):
        query = text("INSERT INTO reviews(username, rating, review_content, isbn) VALUES (:username, :rating, :review_content, :isbn);")
        try:
            self.db.execute(query, {'username': username, 'rating': rating, 'review_content': review_content, 'isbn': isbn})
            self.db.commit()
            return True
        except Exception as e:
            print(e)
            return False

