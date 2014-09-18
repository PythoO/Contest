__author__ = 'pythoo'
from app import db


class Contest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    role = db.relationship('Role', backref=db.backref('contest', lazy='dynamic'))
    campaigns = db.relationship('CampaignMonitor', backref='contest', lazy='select')


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))


class CampaignMonitor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    contest_id = db.Column(db.Integer, db.ForeignKey('contest.id'))


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(80))
    password = db.Column(db.String(80))
