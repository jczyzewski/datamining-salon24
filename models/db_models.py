from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base

from crawler import settings


Base = declarative_base()


def db_connect():
    return create_engine(URL(**settings.DATABASE))