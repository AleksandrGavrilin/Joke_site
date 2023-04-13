from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, ForeignKey


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
    userid = Column(Integer, ForeignKey('Users.id'))
    cat = Column(Integer, ForeignKey("category.id"))
    text = Column(String, default="")


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
    administrator = Column(Boolean, default=False)


class Ratings(Base):
    __tablename__ = "ratings"
    id = Column(Integer, primary_key=True, index=True)
    anek_id = Column(Integer, ForeignKey('anek.id'))
    user_id = Column(Integer, ForeignKey('Users.id'))
    rating = Column(Integer, default=0)


