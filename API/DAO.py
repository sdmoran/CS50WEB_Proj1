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

    def get_bookinfo(self, isbn):
        ### TODO make this real sql not sqlalchemy
        return self.db.query(Book).filter_by(isbn=isbn).first()

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