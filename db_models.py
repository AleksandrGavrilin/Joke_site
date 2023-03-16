from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine


sqlite_database = "sqlite:///aneks.db"


# Создание базы данных:
Base = declarative_base()
engine = create_engine(sqlite_database)


class Joke(Base):
    __tablename__ = "anek"

    id = Column(Integer, primary_key=True, index=True)
    cat = Column(Integer)
    text = Column(String, default="")


class NewAnek(Base):
    __tablename__ = "new_anek"

    id = Column(Integer, primary_key=True, index=True)
    cat = Column(Integer)
    text = Column(String, default="")
    email = Column(String, default="")


class Cat(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, default="")


class Users(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, default="")
    password = Column(String, default="")
    email = Column(String, default="")
    first_name = Column(String, default="")
    second_name = Column(String, default="")

