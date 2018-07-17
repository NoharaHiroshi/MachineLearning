# encoding=utf-8

from base import Base
from session import engine
from image_color import *


def create_all_tables():
    Base.metadata.create_all(engine)

if __name__ == '__main__':
    create_all_tables()
