from flask import Flask, render_template, request, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField, SelectField, TextAreaField
from wtforms.validators import DataRequired, email, Length
import os
import random
import time
from sqlalchemy.orm import sessionmaker
from db_models import *

app = Flask(__name__)
# Список тематики, с отправкой в отдельную таблицу;
# Ваша оценка: Оценка в 5 звезд просмотр и установка пользователем
# Средняя оценка: анекдота (в зависимости от рейтинга, меняется цвет)


def get_cat():
    with Session() as db:
        cats = db.query(Cat).all()
        return [c.name for c in cats]


# Страница с анекдотами:
@app.route('/', methods=['GET', 'POST'])
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


@app.route('/rating/', methods=['POST'])
def rating():
    if request.method == 'POST':
        print(request.form.to_dict())
    return redirect('/')


@app.route('/new/', methods=['GET', 'POST'])
def new_joke():
    flag = False
    form = NewJokeForm()
    if form.validate_on_submit():
        email = form.email.data
        category = form.category.data
        text = form.new_anek.data
        with Session() as db:
            catid = db.query(Cat).filter(Cat.name == category).first().id
            new_anek = NewAnek(cat=catid, email=email, text=text)
            db.add(new_anek)
            db.commit()
        flag = True
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
        print(username)
        print(password)
        print(remember_me)
        return redirect('/')

    return render_template('login.html', form=form)


@app.route('/registration/', methods=['GET', 'POST'])
def registration():
    flag = False
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        password_confrim = form.password_confrim.data
        email = form.email.data
        first_name = form.first_name.data
        second_name = form.second_name.data
        with Session() as db:
            check_email = db.query(Users).filter(Users.email == email).first()
            if check_email:
                flag = True
            else:
                users = Users(email=email, username=username, password=password,
                              first_name=first_name, second_name=second_name)
                db.add(users)
                db.commit()
    return render_template('registration.html', flag=flag, form=form)


class Config:
    SECRET_KEY =os.environ.get('SECRET_KEY') or "you-will-never-guess"


class LoginForm(FlaskForm):
    username = StringField('Логин:', validators=[DataRequired(), Length(max=20)])
    password = PasswordField('Пароль:', validators=[DataRequired(), Length(min=6, max=20)])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RegistrationForm(FlaskForm):
    username = StringField('Ваш логин:', validators=[DataRequired(), Length(max=20)])
    password = PasswordField('Новый пароль:', validators=[DataRequired(), Length(min=6, max=20)])
    password_confrim = PasswordField('Повторите новый пароль:', validators=[DataRequired(), Length(min=6, max=20)])
    email = EmailField('Ваш E-mail:', validators=[DataRequired(),  email(), Length(max=50)])
    first_name = StringField('Ваша имя:', validators=[DataRequired(), Length(max=20)])
    second_name = StringField('Ваша Фамилия:', validators=[DataRequired(), Length(max=20)])
    submit = SubmitField('Зарегистрироваться!')


app.config.from_object(Config)


Base.metadata.create_all(bind=engine)
Session = sessionmaker(autoflush=False, bind=engine)

l1 = get_cat()


class NewJokeForm(FlaskForm):
    email = EmailField('Ваш E-mail:', validators=[DataRequired(), email(), Length(max=50)])
    category = SelectField('Категории:', choices=l1)
    new_anek = TextAreaField('Ваш анекдот:', validators=[DataRequired(), Length(max=500)])
    send = SubmitField('Отправить')


if __name__ == '__main__':
    app.run(debug=True)




