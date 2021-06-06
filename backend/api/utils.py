import crud

from jwt import PyJWTError
from typing import Optional

from access_token import decode_access_token
from models import db

import logging

logger = logging.getLogger(__name__)


def auth_token(token: str) -> bool:
    try:
        payload = decode_access_token(token)

        username = payload.get("sub")
        if username is None:
            return False
    except PyJWTError:
        return False

    user = crud.get_user_by_username(db=db, username=username)
    if user is None:
        return False

    return True
