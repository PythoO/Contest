import models

__author__ = 'pythoo'

from functools import wraps
import flask
from flask import Flask, render_template, request, Response, session, flash, redirect, url_for, jsonify
import flask.ext.sqlalchemy
import flask.ext.restless
import time
from itsdangerous import JSONWebSignatureSerializer

app = Flask(__name__)
# TODO: Move into config file
app.secret_key = 'super_secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'

db = flask.ext.sqlalchemy.SQLAlchemy(app)


def get_token():
    try:
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user.email != email:
            return False
        elif user.password != password:
            return False
        else:
            s = JSONWebSignatureSerializer('secret_key')
            s.dumps({'token': 'a5sedrfd'})
            user.token = s
            user.token_expiration = time.time() + 600
            db.session.commit()
            return s
    except ValueError as e:
        app.logger.debug(e.message)
        return False


def check_token(**kwargs):
    app.logger.debug(kwargs)
    app.logger.debug(request.form['token'])
    try:
        s = JSONWebSignatureSerializer('secret_key')
        data = s.loads(request.form['token'])
        pass
    except ValueError as e:
        app.logger.debug(e.message)
        return jsonify({'response': 'Bad Token'})


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
    token = db.Column(db.Integer)
    token_expiration = db.Column(db.Integer)

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

manager.create_api(Role, methods=['GET', 'POST', 'DELETE', 'PUT'], preprocessors={
    'GET_SINGLE': [check_token],
    'GET_MANY': [check_token],
    'DELETE': [check_token],
    'POST': [check_token]
})
manager.create_api(User, methods=['GET', 'POST', 'DELETE'], exclude_columns=['password'])


@app.route("/token", methods=['POST'])
def api_token():
    token = get_token()
    if not token:
        flash('Oups')
        return jsonify(token='oups')
    else:
        return jsonify(token=token)


@app.route("/login_check", methods=['POST'])
def login_check():
    token = get_token()
    if not token:
        flash('Oups')
        return render_template(url_for('login'))
    else:
        return render_template(url_for('users'))


@app.route('/admin/users')
def users():
    return render_template('admin/user/users.html')


@app.route('/admin/roles')
def roles():
    return render_template('admin/role/roles.html')


if __name__ == '__main__':
    app.debug = True
    app.run()