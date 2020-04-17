from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class ChangeInfoForm(FlaskForm):
    name = StringField('New name')
    surname = StringField('New surname')
    country = StringField('New country')
    city = StringField('New city')
    email = EmailField('New email')
    submit = SubmitField('Change')