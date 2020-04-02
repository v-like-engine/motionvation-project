from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, SubmitField, StringField
from wtforms.validators import DataRequired, NumberRange


class RegisterForm(FlaskForm):
    email = TextField('Почта', validators=[DataRequired()])
    name = StringField('Имя пользователя', validators=[DataRequired()])
    surname = StringField('Фамилия пользователя', validators=[DataRequired()])
    country = StringField('Страна', validators=[DataRequired()])
    city = StringField('Город', validators=[DataRequired()])
    age = StringField('Возраст', validators=[DataRequired(), NumberRange(1, 200)])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')
