from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import Required


class ChalForm(FlaskForm):
    value = IntegerField("Value", validators=[Required()])
    submit = SubmitField('Submit')


class FlagForm(FlaskForm):
    submit = SubmitField('Gen_Flag')
