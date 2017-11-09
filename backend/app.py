from flask import Flask, abort
from playhouse.flask_utils import FlaskDB
from playhouse.shortcuts import model_to_dict

from backend.models import db, Book, Category
from backend.utils import json_response

app = Flask(__name__)
db_wrapper = FlaskDB(app=app, database=db)


@app.route('/books/')
@json_response
def books():
    return [model_to_dict(book) for book in Book.select()]


@app.route('/books/<int:book_id>/')
@json_response
def book(book_id):
    try:
        book = Book.get(Book.id == book_id)
    except Book.DoesNotExist:
        abort(404, 'Book with id=%r does not exists' % book_id)
    else:
        return model_to_dict(book)


@app.route('/categories/')
@json_response
def categories():
    return [model_to_dict(category) for category in Category.select()]


@app.route('/categories/<int:category_id>/')
@json_response
def category(category_id):
    try:
        category = Category.get(Category.id == category_id)
    except Book.DoesNotExist:
        abort(404, 'Category with id=%r does not exists' % category_id)
    else:
        return model_to_dict(category)


if __name__ == '__main__':
    app.run(debug=True)
