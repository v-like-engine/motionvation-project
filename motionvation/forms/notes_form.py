from flask_wtf import FlaskForm
from wtforms import TextField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class NotesForm(FlaskForm):
    title = TextField('Title', validators=[DataRequired(), Length(max=60, message='Maximum 60 symbols')])
    text = TextAreaField('Text', validators=[DataRequired(), Length(max=600, message='Maximum 600 symbols')])
    submit = SubmitField('Add new note')