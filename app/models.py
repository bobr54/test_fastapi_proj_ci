from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    cooking_time = Column(Integer, nullable=False)
    views = Column(Integer, default=0)
    ingredients = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
