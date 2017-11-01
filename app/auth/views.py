from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, \
    current_user
from . import auth
from .. import db
from ..models import User, Team, Flag, Solve, Chal, Role
from .forms import LoginForm, RegistrationForm, JoinTeamForm, CreateTeamForm


@auth.before_app_request
def before_request():
    if current_user.is_authenticated \
            and not current_user.has_team() \
            and request.endpoint[:5] != 'auth.' \
            and request.endpoint != 'static':
        return redirect(url_for('auth.join_team'))


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # admin = False
        # if not User.query.first():
        #     admin = True
        user = User(name=form.username.data,
                    password=form.password.data,
                    stu_id=form.stu_id.data
                    )
        db.session.add(user)
        db.session.commit()
        flash('Register Success.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@auth.route('/join_team', methods=['GET', 'POST'])
@login_required
def join_team():
    form = JoinTeamForm()
    if form.validate_on_submit():
        team = Team.query.filter_by(key=form.teamkey.data).first()
        if team is not None:
            is_admin = False
            if team.id == 1:
                is_admin = True
            role = Role(user=current_user.name, team=team.name, is_admin=is_admin)
            db.session.add(role)
            db.session.commit()
            flash('Join Success')
            return redirect(url_for('main.index'))
        flash('Invalid Team key.')
    return render_template('auth/join_team.html', form=form)


@auth.route('/create_team', methods=['GET', 'POST'])
@login_required
def create_team():
    form = CreateTeamForm()
    if form.validate_on_submit():
        team = Team(name=form.teamname.data,
                    gen_key=form.teamname.data)
        db.session.add(team)
        db.session.commit()
        team = Team.query.filter_by(name=form.teamname.data).first()
        is_admin = False
        if team.id == 1:
            is_admin = True
        role = Role(user=current_user.name, team=team.name, is_admin=is_admin)
        db.session.add(role)
        db.session.commit()
        flash('Create Success')
        return redirect(url_for('main.index'))
    return render_template('auth/create_team.html', form=form)
