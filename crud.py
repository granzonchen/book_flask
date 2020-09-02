import orm
from orm import *
from sqlalchemy import or_


def InsertBook(book_name, publish, title, author):
    with session_scope() as session:
        book = orm.BookInfo(book_name=book_name,
                            publish=publish, title=title, author=author)
        session.add(book)


def GetBook(id=None, book_name=book_name):
    with session_scope() as session:
        return session.query(orm.BookInfo).filter(or_(orm.BookInfo.id == id, orm.BookInfo.book_name == book_name)).first()


def DeleteBook(book_name):
    with session_scope() as session:
        book = GetBook(book_name=book_name)
        if book:
            session.delete(book)


def UpdateBook(id, book_name, publish, title, author):
    with session_scope() as session:
        book = session.query(orm.BookInfo).filter(
            orm.BookInfo.id == id).first()
        if not book:
            return
        