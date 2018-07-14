# coding=utf-8

import contextlib
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

DEBUG = False

DB = 'machine_learning_dev'
HOST = '127.0.0.1'
USER = 'root'
PASSWORD = '123456'
# 默认使用mysql-python包
CONNECT_STRING = 'mysql://%s:%s@%s/%s?charset=utf8' % (USER, PASSWORD, HOST, DB)

engine = create_engine(
    CONNECT_STRING,
    echo=DEBUG,
    pool_recycle=3600,
    pool_size=5
)

Session = sessionmaker(bind=engine, autocommit=True)


@contextlib.contextmanager
def get_session(auto_commit=False):
    """
    session 的 contextmanager， 用在with语句
    """
    session = Session(autocommit=auto_commit)
    try:
        yield session
    except Exception as e:
        session.rollback()
        print 'CANT GET SESSION, ERROR: '
        print e
        raise
    finally:
        session.close()