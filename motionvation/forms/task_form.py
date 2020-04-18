from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length


class TaskForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=100,
                                                                                   message='Maximum 100 symbols')])
    description = TextAreaField('Description', validators=[DataRequired(),
                                                           Length(max=200, message='Maximum 200 symbols')])
    priority = SelectField('Priority', choices=[('10', '10'), ('9', '9'), ('8', '8'), ('7', '7'),
                                                ('6', '6'), ('5', '5'), ('4', '4'), ('3', '3'), ('2', '2'), ('1', '1')],
                           default='5')
    submit = SubmitField('Add')
