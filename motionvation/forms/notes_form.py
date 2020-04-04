from flask_wtf import FlaskForm
from wtforms import TextField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class NotesForm(FlaskForm):
    title = TextField('Title', validators=[DataRequired()])
    text = TextAreaField('Text')
    submit = SubmitField('Add new note')