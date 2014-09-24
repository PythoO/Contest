import models

__author__ = 'pythoo'

from functools import wraps
import flask
from flask import Flask, render_template, request, Response, session, flash, redirect, url_for
import flask.ext.sqlalchemy
import flask.ext.restless
from werkzeug.contrib.cache import SimpleCache

from flask.views import MethodView
cache = SimpleCache()

app = Flask(__name__)
# TODO: Move into config file
app.secret_key = 'super_secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'

db = flask.ext.sqlalchemy.SQLAlchemy(app)


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contact_name = db.Column(db.String(150))
    email = db.Column(db.String(80))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    role = db.relationship('Role', backref=db.backref('users', lazy='dynamic'))
    password = db.Column(db.String(80))

    def __init__(self, contact_name, email, role_id, password):
        self.contact_name = contact_name
        self.email = email
        self.role_id = role_id
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.contact_name


class Contest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True)
    home_text = db.Column(db.Text())
    participation_text = db.Column(db.Text())
    thanks_text = db.Column(db.Text())
    mail_campaigns = db.relationship('MailCampaign', backref='contest')


class MailCampaign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    contest_id = db.Column(db.Integer, db.ForeignKey('contest.id'))


class Social(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    credentials = db.Column(db.String(255))

db.create_all()
# Create the Flask-Restless API manager.
manager = flask.ext.restless.APIManager(app, flask_sqlalchemy_db=db)

"""
role = Role('ROLE_ADMIN')
user = User('Franck Lebrun', 'flebrun@toto.com', 1, 'bibi')
db.session.add(role)
db.session.add(user)
db.session.commit()
"""

manager.create_api(Role, methods=['GET', 'POST', 'DELETE', 'PUT'])
manager.create_api(User, methods=['GET', 'POST', 'DELETE'], exclude_columns=['password'])


@app.route('/admin/users')
def users():
    return render_template('admin/user/users.html')


@app.route('/admin/roles')
def roles():
    return render_template('admin/role/roles.html')


if __name__ == '__main__':
    app.debug = True
    app.run()