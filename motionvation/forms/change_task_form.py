from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, StringField, SelectField
from wtforms.validators import DataRequired, Length


class ChangeTaskForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=60, message='Maximum 60 symbols')])
    description = TextAreaField('Description', validators=[DataRequired(), Length(max=600, message='Maximum 600 symbols')])
    priority = SelectField('Priority', choices=[('10', '10'), ('9', '9'), ('8', '8'), ('7', '7'),
                                                ('6', '6'), ('5', '5'), ('4', '4'), ('3', '3'), ('2', '2'), ('1', '1')],
                           default='5')
    submit = SubmitField('Save changes')