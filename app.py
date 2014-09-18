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
    campaign = MailCampaignModel()
    campaign.name = 'CM'
    db.session.add(campaign)

    role = RoleModel()
    role.name = 'ROLE_ADMIN'
    db.session.add(role)

    contest = ContestModel()
    contest.title = 'My contest title'
    contest.home_text = 'Welcome to my super contest.'
    contest.participation_text = 'Want to participate ? just feed this form.'
    contest.thanks_text = 'Thank you, you\'re participation has been record.<br>Good luck.'
    contest.mail_campaigns.append(campaign)
    contest.role = role.id
    db.session.add(contest)

    user = UserModel()
    user.email = 'tetutetu@yopmail.com'
    user.first_name = 'yop'
    user.last_name = 'mail'
    user.password = 'yop'
    db.session.add(user)

    db.session.commit()
    """
    contest = ContestModel.query.filter_by(id=contest_id).first_or_404()
    """
    # TEST FACTORY
    for camp in contest.mail_campaigns:
        cp = Campaigns()
        cp.campaign_factory(camp.name).call_api()

    """
    """
    db.session.delete(contest)
    db.session.commit()
    """
    return render_template('index.html', contest=contest)


@app.route('/<int:contest_id>/participation')
def participation(contest_id):
    """
    Contest Home Page
    :return:
    """
    contest = ContestModel.query.filter_by(id=contest_id).first_or_404()
    return render_template('participation.html', contest=contest)


@app.route('/<int:contest_id>/thanks')
def thanks(contest_id):
    """
    Contest Home Page
    :return:
    """
    contest = ContestModel.query.filter_by(id=contest_id).first_or_404()
    return render_template('thanks.html', contest=contest)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        form_email = request.form['email']
        form_password = request.form['password']
        user = UserModel.query.filter_by(email=form_email).first()
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
    users = UserModel.query.all()
    return render_template('admin/user/users.html', users=users)


@app.route('/admin/user', methods=['GET', 'POST'])
@login_required
def user_create():
    roles = RoleModel.query.all()
    if request.method == 'POST':
        user = UserModel()
        save_user(user)
        return redirect(url_for('users'))
    return render_template('admin/user/user.html', roles=roles)


@app.route('/admin/user/<int:user_id>', methods=['GET','POST'])
def user_modify(user_id):
    user = UserModel.query.filter_by(id=user_id).first()
    roles = RoleModel.query.all()
    if request.method == 'POST':
        save_user(user)
        return redirect(url_for('users'))
    return render_template('admin/user/user.html', user=user, roles=roles)


@app.route('/admin/user/delete/<int:user_id>')
@login_required
def user_delete(user_id):
    user = UserModel.query.filter_by(id=user_id).first()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('users'))


@app.route('/admin/roles')
@login_required
def roles():
    roles = RoleModel.query.all()
    return render_template('admin/role/roles.html', roles=roles)


@app.route('/admin/role', methods=['GET', 'POST'])
@login_required
def role_create():
    if request.method == 'POST':
        role = RoleModel()
        save_role(role)
        return redirect(url_for('roles'))
    return render_template('admin/role/role.html')


@app.route('/admin/role/<int:role_id>', methods=['GET','POST'])
@login_required
def role_modify(role_id):
    role = RoleModel.query.filter_by(id=role_id).first()
    if request.method == "POST":
        save_role(role)
        return redirect(url_for('roles'))
    return render_template('admin/role/role.html', role=role)


@app.route('/admin/role/delete/<int:role_id>')
@login_required
def role_delete(role_id):
    role = RoleModel.query.filter_by(id=role_id).first()
    db.session.delete(role)
    db.session.commit()
    return redirect(url_for('roles'))


@app.route('/admin/contests')
@login_required
def contests():
    page_contests = cache.get('page_contests')
    if page_contests is None:
        contests = ContestModel.query.all()
        page_contests = render_template('admin/contest/contests.html', contests=contests)
        cache.set('page_contests', page_contests, timeout=2*60)
    return page_contests


@app.route('/admin/contests/<int:contest_id>')
@login_required
def contest_modify(contest_id):
    contest = ContestModel.query.filter_by(id=contest_id).first()
    roles = RoleModel.query.all()
    return render_template('admin/contest/contest.html', contest=contest, roles=roles)


@app.route('/admin/participations')
@login_required
def participations():
    return render_template('admin/participations.html')


def save_user(user):
    """
    Function to save user for create and modify actions
    :param user:
    :return:
    """
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.email = request.form['email']
    user.password = request.form['password']
    user.role_id = request.form['role']
    db.session.add(user)
    db.session.commit()


def save_role(role):
    """
    Function to save role for create and modify actions.
    :param role:
    :return:
    """
    role.name = request.form['name']
    db.session.add(role)
    db.session.commit()

if __name__ == '__main__':
    app.debug = True
    app.run()