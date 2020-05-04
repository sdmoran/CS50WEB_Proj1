import requests
from .permissions import key

url = "https://www.goodreads.com/book/review_counts.json"

def query(isbns):
    resp = requests.get(url, params={
        "key": key,
        "isbns": isbns
    }).json()
    print(resp)
    return resp
    