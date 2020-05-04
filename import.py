import os, csv, sys

from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

db.execute("DROP TABLE books;")
db.execute("DROP TABLE users;")
db.execute("DROP TABLE reviews;")

try:
    db.execute("CREATE TABLE books(isbn VARCHAR(200) PRIMARY KEY, title VARCHAR(200), author VARCHAR(200), year integer);")
    db.execute("CREATE TABLE users(id SERIAL PRIMARY KEY, username VARCHAR(50) UNIQUE NOT NULL, password_hash VARCHAR(355) NOT NULL);")
    db.execute("CREATE TABLE reviews(username VARCHAR(50) REFERENCES user(username), title VARCHAR(200) REFERENCES books(title), review_content TEXT, rating INTEGER, PRIMARY KEY(username, title));")
except Exception as e:
    print(e)
    sys.exit(-1)

print("Succesfully initialized book and user tabless!")

with open('books.csv', 'r') as f:
    reader = csv.reader(f)
    header = next(reader)
    i = 0
    print("Inserting books...")
    for row in reader:
        isbn = row[0]
        title = row[1]
        author = row[2]
        year = row[3]
        i += 1
        query = text("INSERT INTO books VALUES(:isbn, :title, :author, :year);")
        db.execute(query, {'isbn':isbn, 'title':title, 'author':author, 'year':year})
        if i % 500 == 0:
            print(f"{i} done...")
    db.commit()
    print("Successfully inserted books!")