from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length


class TaskForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired(), Length(max=600, message='Maximum 600 symbols')])
    priority = SelectField('Priority', choices=[('High', 'High'), ('Normal', 'Normal'), ('Low', 'Low')])
    submit = SubmitField('Add')