from flask import render_template, url_for, flash, redirect
from . import main
from ..models import User, Team, Flag, Solve, Chal, Role
from flask_login import login_required, current_user
from .forms import FlagForm
from datetime import datetime
from .. import db


@main.route('/')
def index():
    return render_template('main/index.html')


@main.route('/teams')
@login_required
def teams():
    teams = Team.query.order_by(Team.score.desc())
    return render_template('main/teams.html', teams=teams)


@main.route('/flag', methods=['GET', 'POST'])
def flag():
    form = FlagForm()
    if current_user.is_authenticated and current_user.has_team():
        form.team_name.data = current_user.team.name
    if form.validate_on_submit():
        team = Team.query.filter_by(name=form.team_name.data).first()
        flag = Flag.query.filter_by(flag_now=form.flag.data).first()
        if team != None and flag != None:
            used = Solve.query.filter_by(flag_used=flag.flag_now, team_name=team.name).first()
            if used == None:
                solve = Solve(  team_name=team.name,
                                flag_id=flag.id,
                                flag_used=form.flag.data
                                )
                db.session.add(solve)
                db.session.commit()
                team.update_score(flag.chal.value)
                flash('Right')
                return redirect(url_for('.flag'))
            flash('Already Submit')
        else:
            flash('Wrong')
    return render_template('main/flag.html', form=form)


@main.route('/chals')
@login_required
def chals():
    chals = Chal.query.all()
    return render_template('main/chals.html', chals=chals)
