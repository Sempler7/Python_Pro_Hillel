import os
import random
from typing import List, Tuple, Union

from flask import Flask, render_template, redirect, url_for, request, Response
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from sqlalchemy import or_
from wtforms import StringField, IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, NumberRange, Optional
from faker import Faker
from dotenv import load_dotenv

BOOK_GENRES: List[Tuple[str, str]] = [
    ("", "All Genres"),
    ("unspecified", "Unspecified"),
    ("romance", "Romance"),
    ("fantasy", "Fantasy"),
    ("thriller", "Thriller"),
    ("science fiction", "Science Fiction"),
    ("historical fiction", "Historical Fiction"),
    ("biography", "Biography"),
    ("other", "Other"),
]

app = Flask(__name__)

load_dotenv()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

db = SQLAlchemy(app)

fake = Faker()


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer)
    genre = db.Column(db.String(50))

    def __repr__(self) -> str:
        return f"<Book {self.title} by {self.author}>"


def generate_book(count: int = 10) -> None:
    for _ in range(count):
        book = Book(
            title=fake.sentence(nb_words=3),
            author=fake.name(),
            year=fake.random_int(min=1900, max=2026),
            genre=random.choice(BOOK_GENRES[1:])[0],
        )
        db.session.add(book)
    db.session.commit()


class BookForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=1, max=150)],
                        render_kw={"class": "bg-zinc-900 p-2 border border-zinc-300 "
                                            "rounded-md text-zinc-300 w-[30rem]"})
    author = StringField('Author', validators=[DataRequired(), Length(min=1, max=100)],
                         render_kw={"class": "bg-zinc-900 p-2 border border-zinc-300"
                                             " rounded-md text-zinc-300 w-[30rem]"})
    year = IntegerField('Year', validators=[Optional(), NumberRange(min=1800, max=2026)],
                        render_kw={"class": "bg-zinc-900 p-2 border border-zinc-300 rounded-md "
                                            "text-zinc-300"})
    genre = SelectField('Genre', choices=BOOK_GENRES[1:],
                        render_kw={"class": " appearance-none bg-zinc-900 p-2 "
                                            "border border-zinc-300 rounded-md text-zinc-300"})
    submit = SubmitField('Submit', render_kw={
        "class": "py-4 px-8 border border-indigo-500 bg-indigo-500 rounded-md text-zinc-900 "
                 "hover:bg-zinc-900 hover:text-zinc-300"
    })


class SearchFilterForm(FlaskForm):
    q = StringField('Search Book', validators=[Optional(), Length(min=1, max=150)],
                    render_kw={"placeholder": "Search Book",
                               "class": "bg-zinc-900 px-4 py-2 border border-zinc-800 "
                                        "rounded-md text-zinc-300 basis-[40rem] placeholder-zinc-700"})
    genre = SelectField('', choices=BOOK_GENRES, validators=[Optional()],
                        render_kw={"onchange": "this.form.submit()",
                                   "class": "bg-indigo-500 appearance-none border "
                                            "border-indigo-500 rounded-md text-zinc-900 p-4"})


@app.route('/add', methods=['GET', 'POST'])
def add_book() -> Union[str, Response]:
    form = BookForm()

    if form.validate_on_submit():
        print("Form data:", form.title.data, form.author.data, form.year.data)
        new_book = Book(
            title=form.title.data,
            author=form.author.data,
            year=form.year.data,
            genre=form.genre.data
        )
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('list_books'))
    return render_template('add_book.html', form=form)


@app.route('/edit/<int:book_id>', methods=['GET', 'POST'])
def edit_book(book_id) -> Union[str, Response]:
    book = Book.query.get_or_404(book_id)
    form = BookForm(obj=book)

    if form.validate_on_submit():
        book.title = form.title.data
        book.author = form.author.data
        book.year = form.year.data
        book.genre = form.genre.data
        db.session.commit()
        return redirect(url_for('list_books'))
    return render_template('add_book.html', form=form, edit=True)


@app.route('/delete/<int:book_id>', methods=['POST'])
def delete_book(book_id: int) -> Response:

    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('list_books'))


@app.route('/')
def list_books() -> str:

    form = SearchFilterForm(request.args)
    query = Book.query
    filters = []

    if form.q.data:
        filters.append(or_(Book.title.ilike(f"%{form.q.data}%"),
                           Book.author.ilike(f"%{form.q.data}%")))

    if form.genre.data:
        filters.append(Book.genre == form.genre.data)

    if filters:
        query = query.filter(*filters)

    books = query.all()
    return render_template('list_books.html', books=books, form=form)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

        if not Book.query.first():
            generate_book(20)

    app.run(debug=True)
