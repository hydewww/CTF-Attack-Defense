from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import Required, Length, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User, Team, Role


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[Required(), Length(1, 64)])
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
        Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          'Usernames must have only letters, '
                                          'numbers, dots or underscores')])
    password = PasswordField('Password', validators=[
        Required(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[Required()])
    stu_id = IntegerField('Student_ID', validators=[Required()])
    submit = SubmitField('Register')

    def validate_username(self, field):
        if User.query.filter_by(name=field.data).first():
            raise ValidationError('Username already in use.')

    def validate_stu_id(self, field):
        if User.query.filter_by(stu_id=field.data).first():
            raise ValidationError('Student_ID already in use.')


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
