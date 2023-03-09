from flask import Flask, render_template, request, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField, SelectField, TextAreaField
from wtforms.validators import DataRequired, email
import os
import random
import time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


app = Flask(__name__)
# Список тематики, с отправкой в отдельную таблицу; сделать огранич на длину анекдота.
# Ваша оценка: Оценка в 5 звезд просмотр и установка пользователем
# Средняя оценка: анекдота (в зависимости от рейтинга, меняется цвет)
# html на wtf

sqlite_database = "sqlite:///aneks.db"


def get_cat():
    with Session() as db:
        cats = db.query(Cat).all()
        return [c.name for c in cats]


# Страница с анекдотами:
@app.route('/anekdots/', methods=['GET', 'POST'])
def joke():
    if request.method == 'GET':
        with Session() as db:
            number_of_jokes = db.query(Joke).count()
        l = list(range(1, number_of_jokes+1))
    elif request.method == 'POST':
        with Session() as db:
            cat = int(request.form['category'])
            joke_list = db.query(Joke).filter(Joke.cat == cat).all()
        number_of_jokes = len(joke_list)
        l = [j.id for j in joke_list]
    random.seed(time.time())
    l2 = random.choices(l, k=5)
    with Session() as db:
        jokes = db.query(Joke).filter(Joke.id.in_(l2)).all()
        cats = db.query(Cat).all()
    list_category = [(c.name, c.id) for c in cats]
    list_anek = [(j.text, j.id) for j in jokes]
    return render_template('anek.html', n=number_of_jokes, list_anek=list_anek, category=list_category)


@app.route('/new/', methods=['GET', 'POST'])
def new_joke():
    flag = False
    form = NewJokeForm()
    if form.validate_on_submit():
        email = form.email.data
        category = form.category.data
        new_anek = form.new_anek.data
        print(email)
        print(category)
        print(new_anek)
        flag = True
        # return redirect(url_for('send'))
    return render_template('new.html', form=form, flag=flag)


@app.route('/send/')
def send():
    return render_template('send.html')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember_me = form.remember_me.data
        registration = form.registration.data
        if registration:
            return redirect('/registration/')
        print(username)
        print(password)
        print(remember_me)
        return redirect('/anekdots/')

    return render_template('login.html', form=form)


# Создание базы данных:
Base = declarative_base()
engine = create_engine(sqlite_database)


class Joke(Base):
    __tablename__ = "anek"

    id = Column(Integer, primary_key=True, index=True)
    cat = Column(Integer)
    text = Column(String, default="")


class Cat(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, default="")


class Config:
    SECRET_KEY =os.environ.get('SECRET_KEY') or "you-will-never-guess"


class LoginForm(FlaskForm):
    username = StringField('Логин:', validators=[DataRequired()])
    password = PasswordField('Пароль:', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')
    registration = SubmitField('Регистрация')


app.config.from_object(Config)


Base.metadata.create_all(bind=engine)
Session = sessionmaker(autoflush=False, bind=engine)

l1 = get_cat()


class NewJokeForm(FlaskForm):
    email = EmailField('Ваш E-mail', validators=[DataRequired(), email()])
    category = SelectField('Категории', choices=l1)
    new_anek = TextAreaField('Ваш анекдот', validators=[DataRequired()])
    send = SubmitField('Отправить')


if __name__ == '__main__':
    app.run(debug=True)




