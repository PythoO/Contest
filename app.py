__author__ = 'pythoo'

from functools import wraps
from flask import Flask, render_template, request, Response, session, flash, redirect, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from core.campaign import Campaigns
from werkzeug.contrib.cache import SimpleCache
cache = SimpleCache()

app = Flask(__name__)
# TODO: Move into config file
app.secret_key = 'super_secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)
from models import *


def login_required(f):
    @wraps(f)
    def decorator_function(*args, **kwargs):
        if session.get('logged_in') is None:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorator_function


@app.route('/<contest_id>')
def index(contest_id):
    """
    Contest Home Page
    :return:
    """

    """
    campaign = CampaignMonitor()
    campaign.name = 'MC'
    db.session.add(campaign)

    role = Role()
    role.name = 'ROLE_ADMIN'
    db.session.add(role)

    contest = Contest()
    contest.title = 'My contest title 3'
    contest.campaigns.append(campaign)
    contest.role = role.id
    db.session.add(contest)

    user = User()
    user.email = 'tetutetu@yopmail.com'
    user.first_name = 'yop'
    user.last_name = 'mail'
    user.password = 'yop'
    db.session.add(user)

    db.session.commit()
    """
    contest = Contest.query.filter_by(id=contest_id).first_or_404()
    # TEST FACTORY
    for camp in contest.campaigns:
        cp = Campaigns()
        cp.campaign_factory(camp.name).call_api()

    """
    db.session.delete(contest)
    db.session.commit()
    """
    return render_template('index.html', contest=contest)


@app.route('/participation')
def participation():
    """
    Contest Home Page
    :return:
    """
    return render_template('participation.html')


@app.route('/thanks')
def thanks():
    """
    Contest Home Page
    :return:
    """
    return render_template('thanks.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        form_email = request.form['email']
        form_password = request.form['password']
        user = User.query.filter_by(email=form_email).first()
        if user:
            if form_email != user.email:
                error = 'Oupsss not good.'
            elif form_password != user.password:
                error = 'Oupsss not good.'
            else:
                session['logged_in'] = True
                flash('You were logged in')
                return redirect(url_for('dashboard'))
        else:
            error = 'Oupsss not good 2 .'
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

# ####################################
# Admin
# ####################################


@app.route('/admin')
@login_required
def dashboard():
    return render_template('admin/admin.html')


@app.route('/admin/users/')
@login_required
def users():
    users = User.query.all()
    return render_template('admin/user/users.html', users=users)

@app.route('/admin/user/<int:user_id>', methods=['GET','POST'])
def user_modify(user_id):
    user = User.query.filter_by(id=user_id).first()
    if request.method == 'POST':
        user.first_name = request.form['first_name']
        user.last_name = request.form['last_name']
        user.email = request.form['email']
        user.password = request.form['password']
        db.session.add(user)
        db.session.commit()
    return render_template('admin/user/user.html', user=user)

@app.route('/admin/roles')
@login_required
def roles():
    roles = Role.query.all()
    return render_template('admin/roles.html', roles=roles)


@app.route('/admin/contests')
@login_required
def contests():
    page_contests = cache.get('page_contests')
    if page_contests is None:
        contests = Contest.query.all()
        page_contests = render_template('admin/contests.html', contests=contests)
        cache.set('page_contests', page_contests, timeout=2*60)
    return page_contests


@app.route('/admin/contests/<int:contest_id>')
@requires_auth
def contest_modify(contest_id):
    contest = Contest.query.filter_by(id=contest_id).first()
    roles = Role.query.all()
    return render_template('admin/contest.html', contest=contest, roles=roles)

@app.route('/admin/participations')
@login_required
def participations():
    return render_template('admin/participations.html')


if __name__ == '__main__':
    app.debug = True
    app.run()