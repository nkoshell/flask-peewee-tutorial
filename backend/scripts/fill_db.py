import requests
from pprint import pprint  # Pretty-print :)

from playhouse.shortcuts import model_to_dict

from backend.models import Book, Category, db


URL = 'https://oreilly-api.appspot.com/books'


def get_json(url=URL):
    response = requests.get(url=url)
    return response.json()


def get_categories(books):
    return set(book['category'] for book in books)  # Set is unique collection


def save_category(category):
    return Category.create(title=category)


def save_books_categories(books):
    categories = get_categories(books)
    for category in categories:
        db_category = save_category(category)
        print(db_category)


def get_db_categories_as_dict():
    query = Category.select()
    return {category.title: category for category in query}


def save_book(book, categories):
    category = categories.get(book['category'])
    if not category:
        print('Not found category with title: %r' % book['category'])
        return  # Equal `return None`

    return Book.create(title=book['title'], description=book['description'], category=category, url=book['url'])


def save_books(books):
    title2category = get_db_categories_as_dict()
    for book in books:
        db_book = save_book(book, title2category)
        print(db_book)


def get_db_books():
    query = Book.select()
    return [model_to_dict(book) for book in query]


def import_books(books):
    save_books_categories(books)
    save_books(books)
    return get_db_books()


def clear_db():
    db.truncate_tables([Book, Category], restart_identity=True, cascade=True)


if __name__ == '__main__':
    clear_db()
    books = get_json()
    import_books(books)
    db_books = get_db_books()
    pprint(db_books)
