from flask import render_template, url_for, flash, redirect, jsonify
from . import main
from ..models import User, Team, Flag, Solve, Chal, Role
from flask_login import login_required, current_user
from .forms import FlagForm
from datetime import datetime
from .. import db


@main.route('/')
def index():
    members = None
    if current_user.is_authenticated:
        members = Role.query.filter_by(team=current_user.team.name)
    return render_template('main/index.html', members=members)


@main.route('/team/<int:id>')
@login_required
def team(id):
    team = Team.query.filter_by(id=id).first()
    members = None
    if team:
        members = Role.query.filter_by(team=team.name)
    return render_template('main/team.html', team=team, members=members)


@main.route('/teams')
@login_required
def teams():
    teams = Team.query.all()
    return render_template('main/teams.html', teams=teams)


@main.route('/flag', methods=['GET', 'POST'])
def flag():
    form = FlagForm()
    if current_user.is_authenticated and current_user.has_team():
        form.team_name.data = current_user.team.name
    if form.validate_on_submit():
        team = Team.query.filter_by(name=form.team_name.data).first()
        flag = Flag.query.filter_by(flag_now=form.flag.data).first()
        if team != None and flag != None and flag.team_name != team.name:
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


def get_standings(count=None):
    standings_query = db.session.query(
        Team.id.label('teamid'),
        Team.name.label('name'),
        Team.score.label('score')
    )\
        .order_by(Team.score.desc())

    if count:
        standings = standings_query.limit(count).all()
    else:
        standings = standings_query.all()

    return standings

@main.route('/scoreboard')
@login_required
def scoreboard():
    standings = get_standings()
    return render_template('main/scoreboard.html', teams=standings)


@main.route('/scores')
def scores():
    json = {'standings': []}
    standings = get_standings()
    for i, x in enumerate(standings):
        json['standings'].append({'pos': i + 1, 'id': x.teamid, 'team': x.name, 'score': int(x.score)})
    return jsonify(json)


def unix_time(dt):
    return int((dt - datetime(1970, 1, 1)).total_seconds())

@main.route('/top/<int:count>')
@login_required
def topteams(count):
    json = {'places': {}}
    if count > 20 or count < 0:
        count = 10

    standings = get_standings(count=count)
    for i, team in enumerate(standings):
        solves = Solve.query.filter_by(team_name=team.name).all()

        json['places'][i + 1] = {
            'id': team.teamid,
            'name': team.name,
            'solves': []
        }
        for x in solves:
            json['places'][i + 1]['solves'].append({
                'chal': x.flag.chal.id,
                'team': x.team.id,
                'value': x.flag.chal.value,
                'time': unix_time(x.date)
            })
        json['places'][i + 1]['solves'] = sorted(json['places'][i + 1]['solves'], key=lambda k: k['time'])
    return jsonify(json)
