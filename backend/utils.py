from functools import wraps
from flask import jsonify
from werkzeug.exceptions import HTTPException


def json_response(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            response = jsonify(f(*args, **kwargs))
        except Exception as ex:
            response = jsonify(message=str(ex))
            response.status_code = ex.code if isinstance(ex, HTTPException) else 500
        return response
    return wrapper
