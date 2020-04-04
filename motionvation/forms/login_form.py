from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    email = TextField('E-mail', validators=[DataRequired()])
    password = PasswordField('Password')
    submit = SubmitField('Enter')