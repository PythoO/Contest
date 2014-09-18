__author__ = 'pythoo'
from app import db


class RoleModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))


class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(80))
    role_id = db.Column(db.Integer, db.ForeignKey('role_model.id'))
    role = db.relationship('RoleModel', backref=db.backref('users', lazy='dynamic'))
    password = db.Column(db.String(80))


class ContestModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True)
    home_text = db.Column(db.Text())
    participation_text = db.Column(db.Text())
    thanks_text = db.Column(db.Text())
    mail_campaigns = db.relationship('MailCampaignModel', backref='contest')


class MailCampaignModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    contest_id = db.Column(db.Integer, db.ForeignKey('contest_model.id'))


class SocialModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    credentials = db.Column(db.String(255))



