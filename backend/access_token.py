import jwt
import os

from datetime import timedelta, datetime
from typing import Optional

import crud
from models import db_session, User

import logging

logger = logging.getLogger(__name__)

db = db_session.session_factory()

secret_key = os.environ.get("SECRET_KEY")
if secret_key is None:
    secret_key = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"

algorithm = "HS256"

EXPIRE_TIME = 60 * 24 * 30  # a month


def create_access_token(*, data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()

    # set time
    now = datetime.utcnow()

    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=EXPIRE_TIME)

    to_encode.update({"exp": expire, "iat": now, "iss": "biolab-database"})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt


def create_access_token_with_username(username: str):
    data = {"sub": username}

    return create_access_token(data=data)


def decode_access_token(*, token: str):
    to_decode = token
    return jwt.decode(to_decode, secret_key, algorithms=algorithm)


def check_access_token(token: str) -> Optional[User]:
    try:
        payload = decode_access_token(token=token)

        username = payload.get("sub")
        if username is None:
            return False
    except jwt.PyJWTError:
        return False

    user = crud.get_user_by_username(db=db, username=username)
    return user
