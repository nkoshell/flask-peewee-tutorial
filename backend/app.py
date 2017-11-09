from flask import Flask
from playhouse.flask_utils import FlaskDB

from backend.models import db
from backend.views import BookModelApiView, CategoryModelApiView

app = Flask(__name__)
db_wrapper = FlaskDB(app=app, database=db)

book_view = BookModelApiView.as_view('books')
category_view = CategoryModelApiView.as_view('categories')

app.add_url_rule(
    rule='/books/',
    view_func=book_view,
    defaults={'book_id': None},
    methods=['GET']
)

app.add_url_rule(
    rule='/books/<int:book_id>',
    view_func=book_view,
    methods=['GET']
)
app.add_url_rule(
    rule='/categories/',
    view_func=category_view,
    defaults={'category_id': None},
    methods=['GET']
)

app.add_url_rule(
    rule='/categories/<int:category_id>',
    view_func=category_view,
    methods=['GET']
)


if __name__ == '__main__':
    app.run(debug=True)
