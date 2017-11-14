from flask import Flask
from flask_cors import CORS
from playhouse.flask_utils import FlaskDB

from backend.models import db, Book, Category
from backend.views import ApiModelView

app = Flask(__name__)
db_wrapper = FlaskDB(app=app, database=db)
CORS(app)

ApiModelView.register(app, Book, endpoint='books')
ApiModelView.register(app, Category, endpoint='categories')

if __name__ == '__main__':
    app.run(debug=True)
