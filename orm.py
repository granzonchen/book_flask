# ！-*- coding:utf-8 -*-
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from contextlib import contextmanager


Base = declarative_base()


class BookInfo(Base):
    __tablename__ = "bookinfo"

    id = Column(Integer, primary_key=True)
    book_name = Column(String(50), nullable=False)
    publish = Column(String(50), nullable=False)
    title = Column(String(50))
    author = Column(String(50))

    def get_id(self):
        return self.id


# db_connect_string = ''
db_connect_string = 'postgresql://postgres:postgres@localhost:5432/bookinfo'
# db_connect_string = 'mysql://[user]:[pass]@[domain]:[port]/[dbname]'
# db_connect_string = 'sqlite://[file_pathname]'
ssl_args = ''
engine = create_engine(db_connect_string)
SessionType = scoped_session(sessionmaker(bind=engine, expire_on_commit=False))


def get_session():
    return SessionType()


@contextmanager
def session_scope():
    session = get_session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
