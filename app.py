from flask import Flask, render_template, request,redirect, url_for, flash
import os
from datetime import datetime
from data_models import db, Author, Book

app = Flask(__name__)

app.config['SECRET_KEY'] = 'my-super-secret-key'

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/library.sqlite')}"

db.init_app(app)

"""with app.app_context():
    db.create_all()"""


@app.route("/add_author", methods = ['GET', 'POST'])
def add_author():
  """This method adds a new author if request is POST,
  otherwise returns all authors if it is a GET request"""

  if request.method == 'POST':
      name = request.form.get("name")
      birth_date = request.form.get("birth_date")
      date_of_death = request.form.get("date_of_death")

      author = Author(name = name,
                      birth_date = birth_date,
                      date_of_death = date_of_death)

      db.session.add(author)
      db.session.commit()
      flash("Author added successfully", "success")
      return redirect(url_for("add_author"))

  return render_template('add_author.html')



@app.route("/add_book", methods = ['GET', 'POST'])
def add_book():
    """This method adds a new book if request is POST,
      otherwise returns all books if it is a GET request"""

    if request.method == 'POST':
        isbn = request.form.get("isbn")
        title = request.form.get("title")
        publication_year = int(request.form.get("publication_year"))
        author_id = int(request.form.get("author_id"))

        print(request.form)

        book = Book(isbn = isbn,
              title = title,
              publication_year = publication_year,
              author_id = author_id)

        db.session.add(book)
        db.session.commit()
        flash("Book added successfully", "success")
        return redirect(url_for("add_book"))

    authors = Author.query.all()
    return  render_template ('add_book.html', authors = authors)


@app.route("/delete/<int:book_id>", methods = ['POST'])
def delete_book(book_id):
    """Delete a book by its id"""

    book = Book.query.get_or_404(book_id)
    author = book.author

    db.session.delete(book)
    #Delete author if they have no more books
    if len(author.books) == 0:
        db.session.delete(author)
    db.session.commit()

    if len(author.books) == 1:
        flash(f"Book '{book.title}' and its author '{author.name}' deleted successfully!", "success")
    else:
        flash(f"Book '{book.title}' deleted successfully!", "success")

    return redirect(url_for("home"))



@app.route("/home", methods = ['GET'])
def home():
    search_term = request.args.get("q")
    sort_by = request.args.get("sort")

    books_query = Book.query.join(Author)

    if search_term:
        books_query = books_query.filter(Book.title.ilike(f"%{search_term}%"))

    if sort_by == "title":
        books_query = books_query.order_by(Book.title)
    elif sort_by == "author":
        books_query = books_query.order_by(Author.name)
    elif sort_by == "publication_year":
        books_query = books_query.order_by(Book.publication_year)
    else:
        books_query = books_query.order_by(Book.id)

    books = books_query.all()
    return render_template('home.html', books = books, sort_by=sort_by, search_term=search_term)






if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)


