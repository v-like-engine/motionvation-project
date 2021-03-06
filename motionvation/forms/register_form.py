from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, SubmitField, StringField
from wtforms.validators import DataRequired, NumberRange


class RegisterForm(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    country = StringField('Country', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_again = PasswordField('Repeat password', validators=[DataRequired()])
    submit = SubmitField('Register!')
