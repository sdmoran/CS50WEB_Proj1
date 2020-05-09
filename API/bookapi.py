import requests, re
from .permissions import key

url = "https://www.goodreads.com/book/review_counts.json"

def query(isbns):
    if not re.match(r'^([\s\d]+)$', isbns):
        return False
    try:
        resp = requests.get(url, params={
            "key": key,
            "isbns": isbns
        }).json()
    except Exception:
        return False
    if len(resp['books']) > 0:
        return resp ['books'][0]
    else:
        return False
    