from flask_wtf import FlaskForm
from sqlalchemy import Column, String
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class TaskForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = Column(String, nullable=True)
    priority = Column(String, nullable=True)
    submit = SubmitField('Add')