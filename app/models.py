from sqlalchemy import Column, Integer, Text, String
from sqlalchemy.orm import Mapped, DeclarativeBase


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
