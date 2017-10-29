from flask import render_template, url_for, flash, redirect
from . import main
from ..models import User, Team, Flag, Solve, Chal
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
    if current_user.is_authenticated and current_user.team_id:
        form.team_name.data = current_user.team.name
    if form.validate_on_submit():
        team = Team.query.filter_by(name=form.team_name.data).first()
        flag = Flag.query.filter_by(flag_now=form.flag.data).first()
        if team != None and flag != None:
            used = Solve.query.filter_by(flag_used=flag.flag_now, team_id=team.id).first()
            if used == None:
                solve = Solve(  team_id=team.id,
                                flag_id=flag.id,
                                flag_used=form.flag.data,
                                date=datetime.now())
                db.session.add(solve)
                db.session.commit()
                # !!!
                team.update_score(flag.chal.value)
                flash('Right')
                return redirect(url_for('.flag'))
            flash('Already Submit')
        else:
            flash('Wrong')
    return render_template('main/flag.html', form=form)
