from data_models import Book, Author

books = Book.query() \
       .filter(Book.title.like('%book%')) \
        .all()