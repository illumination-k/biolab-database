from sqlalchemy import Column, create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, backref

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.functions import func
from sqlalchemy.sql.sqltypes import DateTime, Float, Integer, String, TEXT

engine = create_engine('sqlite:///database.sqlite3', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
# クエリを扱うために宣言
Base.query = db_session.query_property()


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    name = Column(String)


class Primer(Base):
    __tablename__ = "primer"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    desc = Column(TEXT)
    seq = Column(String)
    stock_place = Column(String)
    tm = Column(Float)
    registered = Column(DateTime, default=func.now())
    user = relationship(User, backref=backref('primer', uselist=True, cascade='delete,all'))