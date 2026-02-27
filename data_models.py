from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Author(db.Model):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    birth_date = db.Column(db.String(100))
    date_of_death = db.Column(db.String(100))

    def __repr__(self):
        return f"Author: {self.name}"

    def __str__(self):
        return f"Author: {self.name} born on {self.date_of_death} and died at {self.date_of_death}"




class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    isbn = db.Column(db.String(100))
    title = db.Column(db.String(100))
    publication_year = db.Column(db.Integer)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))

    def __repr__(self):
        return f"Book: {self.title}"

    def __str__(self):
        return f"Book: {self.isbn} with title {self.title} published in the year {self.publication_year}"



