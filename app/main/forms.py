from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required


class FlagForm(FlaskForm):
    team_name = StringField("Team Name", validators=[Required()])
    flag = StringField("Flag", validators=[Required()])
    submit = SubmitField('Submit')
