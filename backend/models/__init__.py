from sqlalchemy import Column, create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, backref

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.functions import func
from sqlalchemy.sql.sqltypes import DateTime, Float, Integer, String, TEXT

Engine = create_engine(
    "postgresql://postgres:postgres@postgres:5432/main", encoding="utf-8", echo=False
)

db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=Engine)
)
Base = declarative_base()
# クエリを扱うために宣言
Base.query = db_session.query_property()


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    permission_level = Column(Integer, default=1)
    registered = Column(DateTime, default=func.now())
    updated = Column(DateTime, default=func.now())


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
    user = relationship(
        User, backref=backref("primer", uselist=True, cascade="delete,all")
    )


class Plasmid(Base):
    __tablename__ = "plasmid"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    desc = Column(TEXT)
    seq = Column(TEXT)
    stock_place = Column(String)
    registered = Column(DateTime, default=func.now())
    updated = Column(DateTime, default=func.now())
    user = relationship(
        User, backref=backref("plasmid", uselist=True, cascade="delete,all")
    )
