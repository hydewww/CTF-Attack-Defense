from flask import render_template, url_for, flash, redirect
from . import admin
from ..models import User, Team, Flag, Solve, Chal
from flask_login import login_required, current_user
from .. import db
from ..decorators import admin_required
from .forms import ChalForm, FlagForm


@admin.route('/chals', methods=['GET', 'POST'])
@admin_required
def chals():
    form = ChalForm()
    chals = Chal.query.all()
    if form.validate_on_submit():
        chal = Chal(value=form.value.data)
        db.session.add(chal)
        db.session.commit()
        flash('Success.')
        return redirect(url_for('.chals'))
    return render_template('admin/chals.html', chals=chals, form=form)


@admin.route('/solves')
@admin_required
def solves():
    solves = Solve.query.all()
    return render_template('admin/solves.html', solves=solves)


@admin.route('/flags', methods=['GET', 'POST'])
@admin_required
def flags():
    form = FlagForm()
    flags = Flag.query.all()
    if form.validate_on_submit():
        chals = Chal.query.all()
        teams = Team.query.all()
        for chal in chals:
            for team in teams:
                if not Flag.query.filter_by(team_id=team.id, chal_id=chal.id).first():
                    flag = Flag(team_id=team.id,
                                chal_id=chal.id)
                    db.session.add(flag)
                    db.session.commit()
        flash("Done")
        return redirect(url_for('.flags'))
    return render_template('admin/flags.html', flags=flags, form=form)
