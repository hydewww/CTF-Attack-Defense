from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import Required, Length, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User, Team, Role


class CreateTeamForm(FlaskForm):
    teamname = StringField('Team Name', validators=[
        Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          'Team Name must have only letters, '
                                          'numbers, dots or underscores')])
    submit = SubmitField('Create')

    def validate_teamname(self, field):
        if Team.query.filter_by(name=field.data).first():
            raise ValidationError('Name already in use.')


class JoinTeamForm(FlaskForm):
    teamkey = StringField('Team key', validators=[
        Required(), Length(1, 64), Regexp('^[A-Za-z0-9]*$', 0,
                                          'Team key must have only letters or numbers')])
    submit = SubmitField('Join')
