from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class ChangeInfoForm(FlaskForm):
    old = StringField('Old', validators=[DataRequired()])
    new = StringField('New', validators=[DataRequired()])
    submit = SubmitField('Add')