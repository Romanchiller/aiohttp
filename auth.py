import bcrypt
from models import MODEL, Token, Session
from aiohttp import request, web
from tools import get_http_error
from sqlalchemy import select


session = Session()


def hash_password(password: str):
    password = password.encode()
    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
    decoded_password = hashed_password.decode()
    return decoded_password


def check_password(password: str, hashed_password: str):
    password = password.encode()
    hashed_password = hashed_password.encode()
    return bcrypt.checkpw(password, hashed_password)
