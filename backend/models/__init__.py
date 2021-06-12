from sqlalchemy import Column, create_engine, ForeignKey
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, backref

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.functions import func
from sqlalchemy.sql.sqltypes import (
    DateTime,
    Float,
    Integer,
    String,
    TEXT,
    Boolean,
    LargeBinary,
)

Engine = create_engine(
    "postgresql://postgres:postgres@postgres:5432/main", encoding="utf-8", echo=False
)

db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=Engine)
)

Base = declarative_base()

# declare for query
Base.query = db_session.query_property()


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String)
    password = Column(TEXT)
    picture = Column(LargeBinary)
    birthday = Column(DateTime)
    permission_level = Column(Integer, default=1)
    registered = Column(DateTime, default=func.now())
    updated = Column(DateTime, default=func.now())
    active = Column(Boolean)

    # child relations
    primer = relationship("Primer")
    plasmid = relationship("Plasmid")


class Tag(Base):
    __tablename__ = "tag"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    desc = Column(TEXT)

    primer = relationship("Primer")
    plasmid = relationship("Plasmid")


class Primer(Base):
    __tablename__ = "primer"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    desc = Column(TEXT)
    seq = Column(String)
    stock_place = Column(String)
    tm = Column(Float)
    registered = Column(DateTime, default=func.now())
    updated = Column(DateTime, default=func.now())

    user_id = Column(Integer, ForeignKey("user.id"))
    tag_id = Column(Integer, ForeignKey("tag.id"))


class Plasmid(Base):
    __tablename__ = "plasmid"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    desc = Column(TEXT)
    gbk = Column(TEXT)
    stock_place = Column(String)
    registered = Column(DateTime, default=func.now())
    updated = Column(DateTime, default=func.now())

    user_id = Column(Integer, ForeignKey("user.id"))
    tag_id = Column(Integer, ForeignKey("tag.id"))
