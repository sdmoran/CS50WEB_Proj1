import os, csv, sys, argparse

from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--drop', dest='drop', action='store_true',
                    help='Whether or not to drop the tables')
args = parser.parse_args()
if args.drop:
    try:
        print("Trying to drop tables...")
        db.execute("DROP TABLE books CASCADE;")
        db.execute("DROP TABLE users CASCADE;")
        db.execute("DROP TABLE reviews CASCADE;")
        db.commit()
        db.close()
    except Exception as e:
        print("Failed to drop tables!")
        print(e)
    db = scoped_session(sessionmaker(bind=engine))

try:
    print("Trying to create tables...")
    db.execute("CREATE TABLE books(isbn VARCHAR(200) UNIQUE PRIMARY KEY, title VARCHAR(200), author VARCHAR(200), year integer);")
    db.execute("CREATE TABLE users(id SERIAL PRIMARY KEY, username VARCHAR(50) UNIQUE NOT NULL, password_hash VARCHAR(355) NOT NULL);")
    db.execute("CREATE TABLE reviews(username VARCHAR(50) REFERENCES users(username), isbn VARCHAR(200) REFERENCES books(isbn), review_content TEXT, rating INTEGER, PRIMARY KEY(username, isbn));")
    db.commit()
    db.close()
except Exception as e:
    print(e)
    sys.exit(-1)

db = scoped_session(sessionmaker(bind=engine))

print("Succesfully initialized book and user tables!")

with open('books.csv', 'r') as f:
    reader = csv.reader(f)
    header = next(reader)
    i = 0
    print("Inserting books...")
    for row in reader:
        print(i)
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