from flask import render_template, redirect, request, url_for, flash, current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from .. import db
from ..models import User
try:
    import urllib.parse
except:
    from urlparse import urlparse
    import urllib


@auth.route('/login')
def login():
    SSO_URL = current_app.config['SSO_URL']
    if not current_user.is_authenticated:
        referer = urllib.parse.quote(url_for('.login', _external=True))
        return redirect(SSO_URL + "/login?referer=" + referer)
    return redirect(url_for('main.index'))


@auth.route('/login/<string:token>')
def token_login(token):
    print(token)
    id = _confirmToken(token)
    user = User.query.filter_by(id=id).first_or_404()
    print(user.id)
    login_user(user)
    return redirect(request.args.get('next') or url_for('main.index'))
    

def _confirmToken(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token.encode())
    except:
        return -1
    return data.get('id')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@auth.route('/register')
def register():
    SSO_URL = current_app.config['SSO_URL']
    if not current_user.is_authenticated:
        referer = urllib.parse.quote(url_for('.login', _external=True))
        return redirect(SSO_URL + "/register?referer=" + referer)
    return redirect(url_for('main.index'))
