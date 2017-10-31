from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import Required, Length


class ChalForm(FlaskForm):
    name = StringField("Name", validators=[Required(), Length(1, 64)])
    port = IntegerField("Port", validators=[Required()])
    value = IntegerField("Value", validators=[Required()])
    submit = SubmitField('Submit')


class FlagForm(FlaskForm):
    submit = SubmitField('Gen_Flag')
