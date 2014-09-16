__author__ = 'pythoo'

from flask import Flask, render_template, request, Response
from flask.ext.sqlalchemy import SQLAlchemy
from core.campaign import Campaigns
from core.authenticate  import *
from werkzeug.contrib.cache import SimpleCache
cache = SimpleCache()

app = Flask(__name__)
# TODO: Move into config file
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)
from models import *


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

# ####################################
# Admin
# ####################################
@app.route('/admin')
@requires_auth
def dashboard():
    return render_template('admin/admin.html')


@app.route('/admin/roles')
@requires_auth
def roles():
    return render_template('admin/roles.html')


@app.route('/admin/users')
@requires_auth
def users():
    return render_template('admin/users.html')


@app.route('/admin/contests')
@requires_auth
def contests():
    page_contests = cache.get('page_contests')
    if page_contests is None:
        contests = Contest.query.all()
        page_contests = render_template('admin/contests.html', contests=contests)
        cache.set('page_contests', page_contests, timeout=2*60)
    return page_contests


@app.route('/admin/participations')
@requires_auth
def participations():
    return render_template('admin/participations.html')


if __name__ == '__main__':
    app.debug = True
    app.run()