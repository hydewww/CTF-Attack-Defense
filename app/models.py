import datetime, hashlib
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app
from flask_login import UserMixin, AnonymousUserMixin
from . import db, login_manager


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    __bind_key__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    stu_id = db.Column(db.Integer, unique=True)
    team = db.relationship('Team',
                            secondary='roles',
                            uselist=False
                            )
    role = db.relationship('Role', backref="users", uselist=False)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        role = Role.query.filter_by(user=self.name).first()
        if role:
            return self.role.is_admin
        return False

    def has_team(self):
        role = Role.query.filter_by(user=self.name).first()
        if role:
            return True
        return False

    def __repr__(self):
        return '<User %r>' % self.name

class AnonymousUser(AnonymousUserMixin):
    def is_admin(self):
        return False

    def has_team(self):
        return False

login_manager.anonymous_user = AnonymousUser

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Team(db.Model):
    __tablename__ = 'teams'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    key = db.Column(db.String(128), unique=True)
    ip = db.Column(db.String(46), unique=True)
    score = db.Column(db.Integer, default=0)
    #users = db.relationship('User', backref='team')
    users = db.relationship('User',
                            secondary='roles'
                            )
    flags = db.relationship('Flag', backref='team')
    solves = db.relationship('Solve', backref='team')

    def __init__(self, **kwargs):
        super(Team, self).__init__(**kwargs)

    @property
    def gen_key(self):
        raise AttributeError('gen_key is not a readable attribute')

    @gen_key.setter
    def gen_key(self, name):
        key = hashlib.md5(name.encode('utf-8')).hexdigest()
        self.key = key

    def update_score(self, value):
        self.score += value
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return '<User %r>' % self.name


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(64), db.ForeignKey("users.name"))
    team = db.Column(db.String(64), db.ForeignKey("teams.name"))
    is_admin = db.Column(db.Boolean, default=False)

    def __init__(self, user, team, is_admin):
        self.user = user
        self.team = team
        self.is_admin = is_admin

    def __repr__(self):
        return '<Role %r>' % self.id


class Chal(db.Model):
    __tablename__ = 'chals'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    port = db.Column(db.Integer, unique=True)
    value = db.Column(db.Integer, default=100)
    flags = db.relationship('Flag', backref='chal')

    def __init__(self, name, port, value):
        self.name = name
        self.port = port
        self.value = value

    def __repr__(self):
        return '<Challenge %r>' % self.name


class Flag(db.Model):
    __tablename__ = 'flags'
    id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.Integer, db.ForeignKey('teams.name'))
    chal_name = db.Column(db.Integer, db.ForeignKey('chals.name'))
    flag_now = db.Column(db.String(64), unique=True)
    solves = db.relationship('Solve', backref='flag')

    def __init__(self, team_name, chal_name):
        self.team_name = team_name
        self.chal_name = chal_name

    def __repr__(self):
        return "<Flag {0} for team {1} challenge {2}>".format(self.flag, self.team_id, self.chal)


class Solve(db.Model):
    __tablename__ = 'solves'
    id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.Integer, db.ForeignKey('teams.name'))
    flag_id = db.Column(db.String(64), db.ForeignKey('flags.id'))
    flag_used = db.Column(db.String(64))
    date = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, team_name, flag_id, flag_used):
        self.team_name = team_name
        self.flag_id = flag_id
        self.flag_used = flag_used

    def __repr__(self):
        return '<Solve %r>' % self.id
