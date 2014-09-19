__author__ = 'pythoo'

from functools import wraps
import flask
from flask import Flask, render_template, request, Response, session, flash, redirect, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug.contrib.cache import SimpleCache

from flask.views import MethodView
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
        app.logger.debug(user.password)
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


@app.route('/admin/roles', methods=['GET', 'POST'])
@login_required
def roles():
    if request.method == 'POST':
        role = RoleModel()
        save_role(role)
        return redirect(url_for('roles'))
    all_roles = RoleModel.query.all()
    return render_template('admin/role/roles.html', roles=all_roles)


@app.route('/admin/roles/<int:role_id>', methods=['GET', 'PUT', 'DELETE'])
@login_required
def roles_modify(role_id):
    role = RoleModel.query.filter_by(id=role_id).first()
    if request.method == "POST":
        save_role(role)
        return redirect(url_for('roles'))
    return render_template('admin/role/role.html', role=role)


@app.route('/admin/contests')
@login_required
def contests():
    page_contests = cache.get('page_contests')
    if page_contests is None:
        all_contests = ContestModel.query.all()
        page_contests = render_template('admin/contest/contests.html', contests=all_contests)
        cache.set('page_contests', page_contests, timeout=2*60)
    return page_contests


@app.route('/admin/contests/<int:contest_id>', methods=['GET', 'PUT', 'DELETE'])
@login_required
def contests_modify(contest_id):
    contest = ContestModel.query.filter_by(id=contest_id).first()
    all_roles = RoleModel.query.all()
    return render_template('admin/contest/contest.html', contest=contest, roles=all_roles)


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
    try:
        if request.form['first_name']:
            user.first_name = request.form['first_name']
        if request.form['last_name']:
            user.last_name = request.form['last_name']
        if request.form['email']:
            user.email = request.form['email']
        if request.form['password']:
            user.password = request.form['password']
        if request.form['role']:
            user.role_id = request.form['role']

        db.session.merge(user)
        db.session.commit()
    except Exception, e:
        app.logger.debug(e.message)


def save_role(role):
    """
    Function to save role for create and modify actions.
    :param role:
    :return:
    """
    role.name = request.form['name']
    db.session.add(role)
    db.session.commit()


class UserAPI(MethodView):

    @login_required
    def get(self, user_id):
        if user_id is None:
            app.logger.debug('GET')
            all_users = UserModel.query.all()
            all_roles = RoleModel.query.all()
            return render_template('admin/user/user.html', users=all_users, roles=all_roles)
        else:
            app.logger.debug('GET USER')
            all_roles = RoleModel.query.all()
            user = UserModel.query.filter_by(id=user_id).first()
            return render_template('admin/user/user.html', user=user, roles=all_roles)

    @login_required
    def post(self):
        app.logger.debug('POST')
        user = UserModel()
        save_user(user)
        all_users = UserModel.query.all()
        all_roles = RoleModel.query.all()
        return render_template('admin/user/user.html', users=all_users, roles=all_roles)

    @login_required
    def delete(self, user_id):
        app.logger.debug('DELETE')
        user = UserModel.query.filter_by(id=user_id).first()
        db.session.delete(user)
        db.session.commit()
        all_users = UserModel.query.all()
        all_roles = RoleModel.query.all()
        return render_template('admin/user/user.html', users=all_users, roles=all_roles)

    @login_required
    def put(self, user_id):
        app.logger.debug('PUT %s' % user_id)
        user = UserModel.query.filter_by(id=user_id).first()
        save_user(user)
        all_users = UserModel.query.all()
        all_roles = RoleModel.query.all()
        return render_template('admin/user/user.html', users=all_users, roles=all_roles)

user_view = UserAPI.as_view('user_api')
app.add_url_rule('/admin/users/', defaults={'user_id': None}, view_func=user_view, methods=['GET'])
app.add_url_rule('/admin/users/', view_func=user_view, methods=['POST'])
app.add_url_rule('/admin/users/<int:user_id>', view_func=user_view, methods=['GET', 'PUT', 'DELETE'])

if __name__ == '__main__':
    app.debug = True
    app.run()