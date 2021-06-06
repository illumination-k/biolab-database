from sqlalchemy.orm import Session
from api import schema
import models
import bcrypt

from typing import Optional


ENCODE = "utf-8"


def get_user_by_username(db: Session, username: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.username == username).first()


def create_user(db: Session, user: schema.CreateUser) -> Optional[models.User]:
    hashed_password = bcrypt.hashpw(user.password.encode(ENCODE), bcrypt.gensalt())

    # decode needs
    # https://stackoverflow.com/questions/34548846/flask-bcrypt-valueerror-invalid-salt/37032208
    db_user = models.User(
        username=user.username, password=hashed_password.decode(ENCODE)
    )
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except:
        db.rollback()


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
