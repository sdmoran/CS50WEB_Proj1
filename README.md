# Project 1
## Sam Moran
Web Programming with Python and JavaScript

## Structure
### HTML Files
#### base.html
Contains basic elements that appear on all pages on the site, such as navbar and a div for body of
each page.

#### book.html
A page that displays information about an individual book, such as title, author, ISBN, reviews, etc.

#### login.html
A page that contains a form with which the user can login to the site.

#### logout.html
A page that contains a simple message indicating that the user has logged out.

#### results.html
A page that displays information about books matching a search query submitted by the user on the
'search' page.

#### search.html
A page that contains a form allowing a user to search for books by author, ISBN or title.

#### signup.html
A page that contains a form allowing the user to signup with a username and password.

### Python Files
#### application.py
Flask app, contains information for routes and logic for handling requests and form submissions.

#### api/bookapi.py
Contains a method for making a call to the goodreads API and parsing the response.

#### api/DAO.py
Class containing various methods for managing and interacting with my database.

#### api/permissions.py
Contains goodreads API key and database url.