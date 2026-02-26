from flask import Flask, render_template, request,redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os
from data_models import db, Author, Book

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/library.sqlite')}"

db.init_app(app)



@app.route("/add_author", methods = ['GET', 'POST'])
def add_author():
  if request.method == 'POST':
      author = Author(name = request.form.get("name"),
                      birth_date = request.form.get("birth_date"),
                      date_of_death = request.form.get("date_of_death"))
      db.session.add(author)
      db.session.commit()
      flash("Author added successfully", "success")
      return redirect(url_for("add_author.html"))

  return render_template('add_author.html')



@app.route("/add_book", methods = ['GET', 'POST'])
def add_author():
  return render_template('add_book.html'),200


"""with app.app_context():
    db.create_all()"""