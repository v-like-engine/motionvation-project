from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, StringField
from wtforms.validators import DataRequired, Length


class ChangeNewsForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=60, message='Maximum 60 symbols')])
    text = TextAreaField('Text', validators=[DataRequired(), Length(max=600, message='Maximum 600 symbols')])
    submit = SubmitField('Save changes')