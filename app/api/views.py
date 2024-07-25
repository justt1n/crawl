# app/api/views.py

from . import api_bp


@api_bp.route('/ping')
def ping():
    print("pong pong")
    return {"message": "pong pong!"}

@api_bp.route('/api/v1/book')
def getBook():
    print("getBook")
    return {"message": "getBook!"}