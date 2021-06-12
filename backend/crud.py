from sqlalchemy import and_
from sqlalchemy.orm import Session
from api import schema
import models
import bcrypt
from graphql import GraphQLError
from typing import Optional, Literal


ENCODE = "utf-8"


def get_user_by_username(db: Session, username: str) -> Optional[models.User]:
    try:
        user = db.query(models.User).filter(models.User.username == username).first()
    except:
        db.rollback()
        raise GraphQLError("get user by username is failed")
    return db.query(models.User).filter(models.User.username == username).first()


KEY_LITERAL = Literal["username", "email"]


def get_user(db: Session, key: KEY_LITERAL, query: str) -> Optional[models.User]:
    try:
        if key == "username":
            user = db.query(models.User).filter(models.User.username == query).first()
        elif key == "email":
            user = db.query(models.User).filter(models.User.email == query).first()
        else:
            raise ValueError("get invalid key")
    except:
        db.rollback()
        raise GraphQLError("crud error: get user is failed")
    return user


def create_user(db: Session, user: models.User) -> Optional[models.User]:
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except:
        db.rollback()
        raise GraphQLError("Error in Creating User")


def check_password(db: Session, username: str, password: str) -> bool:
    db_user = get_user_by_username(db, username)
    return bcrypt.checkpw(password.encode(ENCODE), db_user.password.encode(ENCODE))


def get_primer_by_seq(db: Session, seq: str) -> Optional[models.Primer]:
    return db.query(models.Primer).filter(models.Primer.seq == seq).first()


def create_primer(
    db: Session,
    user: models.User,
    name: str,
    seq: str,
    desc: Optional[str] = None,
    stock_place: Optional[str] = None,
) -> Optional[models.Primer]:
    primer: models.Primer = models.Primer(
        name=name, seq=seq, desc=desc, user_id=user.id
    )

    try:
        db.add(primer)
        db.commit()
        db.refresh(primer)
        return primer
    except:
        db.rollback()
