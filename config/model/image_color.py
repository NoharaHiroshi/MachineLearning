# encoding=utf-8

import traceback
import datetime
from sqlalchemy import Column, BigInteger, Integer, String, DateTime, UniqueConstraint, Float
from config.model.base import Base, IdGenerator


class ImageColor(Base):
    __tablename__ = 'image_color'

    UNKNOWN, RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE, PINK, BROWN, WHITE, BLACK = range(11)

    id = Column(BigInteger, default=IdGenerator.gen, primary_key=True)
    red = Column(Float, default=0, index=True)
    orange = Column(Float, default=0, index=True)
    yellow = Column(Float, default=0, index=True)
    green = Column(Float, default=0, index=True)
    blue = Column(Float, default=0, index=True)
    purple = Column(Float, default=0, index=True)
    pink = Column(Float, default=0, index=True)
    brown = Column(Float, default=0, index=True)
    white = Column(Float, default=0, index=True)
    black = Column(Float, default=0, index=True)
    tag = Column(Integer, default=0, index=True)

