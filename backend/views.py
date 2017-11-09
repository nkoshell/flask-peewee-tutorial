from flask.views import MethodView
from playhouse.shortcuts import model_to_dict
from werkzeug.exceptions import abort

from backend.models import Book, Category
from backend.utils import json_response


class BookModelApiView(MethodView):
    decorators = [
        json_response,
    ]

    def list(self):  # Shortcut
        return [model_to_dict(book) for book in Book.select()]

    def get(self, book_id):
        if book_id is not None:
            try:
                book = Book.get(Book.id == book_id)
            except Book.DoesNotExist:
                abort(404, 'Book with id=%r does not exists' % book_id)
            else:
                return model_to_dict(book, backrefs=True)
        return self.list()


class CategoryModelApiView(MethodView):
    decorators = [
        json_response,
    ]

    def list(self):  # Shortcut
        return [model_to_dict(category) for category in Category.select()]

    def get(self, category_id):
        if category_id is not None:
            try:
                category = Category.get(Category.id == category_id)
            except Book.DoesNotExist:
                abort(404, 'Category with id=%r does not exists' % category_id)
            else:
                return model_to_dict(category, backrefs=True)
        return self.list()
