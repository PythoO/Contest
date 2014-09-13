__author__ = 'pythoo'

from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from core.campaign import Campaigns

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
    contest.title = 'My contest title'
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


if __name__ == '__main__':
    app.debug = True
    app.run()