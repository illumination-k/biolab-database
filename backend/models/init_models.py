import models
import crud
import bcrypt
from typing import Optional
from graphql import GraphQLError

ENCODE = "utf-8"

db = models.db_session.session_factory()


def is_duplicate_email(email: str) -> bool:
    return crud.get_user(db, key="email", query=email) is not None


def is_duplicate_username(username: str) -> bool:
    return crud.get_user(db, key="username", query=username) is not None


def init_user(
    username: str,
    email: str,
    password: str,
    picture: Optional[str] = None,
    permission_level: int = 2,
) -> models.User:
    if is_duplicate_email(email=email):
        raise GraphQLError("Email is duplicated")

    if is_duplicate_username(username=username):
        raise GraphQLError("Username is duplicated")

    # decode needs
    # https://stackoverflow.com/questions/34548846/flask-bcrypt-valueerror-invalid-salt/37032208
    hashed_password = bcrypt.hashpw(password.encode(ENCODE), bcrypt.gensalt()).decode(
        ENCODE
    )
    return models.User(
        username=username,
        email=email,
        password=hashed_password,
        picture=picture,
        permission_level=permission_level,
        active=True,
    )
