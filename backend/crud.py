from sqlalchemy.orm import Session
from api import schema
import models
import bcrypt

from typing import Optional


ENCODE = "utf-8"


def get_user_by_username(db: Session, username: str) -> Optional(models.User):
    return db.query(models.User).filter(models.User.username == username).first()


def create_user(db: Session, user: schema.CreateUser) -> models.User:
    hashed_password = bcrypt.hashpw(user.password.encode(ENCODE), bcrypt.gensalt())
    db_user = models.User(username=user.username, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def check_password(db: Session, username: str, password: str) -> bool:
    db_user = get_user_by_username(db, username)
    return bcrypt.checkpw(password.encode(ENCODE), db_user.password.encode(ENCODE))
