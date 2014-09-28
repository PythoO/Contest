import models

__author__ = 'pythoo'

from functools import wraps
import flask
from flask import Flask, render_template, request, Response, session, flash, redirect, url_for, jsonify
import flask.ext.sqlalchemy
import flask.ext.restless
from flask.ext.restless import ProcessingException
import time
from itsdangerous import JSONWebSignatureSerializer

app = Flask(__name__)
# TODO: Move into config file
app.debug = True
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
            token = s.dumps({'user_id': user.id})
            user.token = token
            user.token_expiration = time.time() + 600
            db.session.commit()
            session['logged_in'] = token
            return token
    except ValueError as e:
        app.logger.debug(e.message)
        return False


def check_token(token=None, **kwargs):
    try:
        token = request.args.get('token')
        s = JSONWebSignatureSerializer('secret_key')
        data = s.loads(token)
        user_id = data['user_id']
        user = User.query.filter_by(id=user_id).first()
        if not user:
            raise ProcessingException(description='Not Authorized', code=401)
        elif user.token != token:
            raise ProcessingException(description='Not Authorized', code=401)
        else:
            pass
    except ValueError as e:
        app.logger.debug(e.message)
        raise ProcessingException(description='Not Authorized', code=401)


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
    'POST': [check_token],
    'DELETE': [check_token],
    'PUT_SINGLE': [check_token]
})

manager.create_api(User, methods=['GET', 'POST', 'DELETE', 'PUT'], exclude_columns=['password'], preprocessors={
    'GET_SINGLE': [check_token],
    'GET_MANY': [check_token],
    'POST': [check_token],
    'DELETE': [check_token],
    'PUT_SINGLE': [check_token]
})

manager.create_api(Contest, methods=['GET', 'POST', 'DELETE', 'PUT'], exclude_columns=['password'], preprocessors={
    'GET_SINGLE': [check_token],
    'GET_MANY': [check_token],
    'POST': [check_token],
    'DELETE': [check_token],
    'PUT_SINGLE': [check_token]
})

manager.create_api(MailCampaign, methods=['GET', 'POST', 'DELETE', 'PUT'], exclude_columns=['password'], preprocessors={
    'GET_SINGLE': [check_token],
    'GET_MANY': [check_token],
    'POST': [check_token],
    'DELETE': [check_token],
    'PUT_SINGLE': [check_token]
})

manager.create_api(Social, methods=['GET', 'POST', 'DELETE', 'PUT'], exclude_columns=['password'], preprocessors={
    'GET_SINGLE': [check_token],
    'GET_MANY': [check_token],
    'POST': [check_token],
    'DELETE': [check_token],
    'PUT_SINGLE': [check_token]
})


@app.route("/token", methods=['POST'])
def api_token():
    token = get_token()
    if not token:
        flash('Oups')
        return jsonify(token='oups')
    else:
        return jsonify(token=token)


@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/login/check", methods=['POST'])
def login_check():
    token = get_token()
    if not token:
        return redirect(url_for('login'))
    else:
        return redirect(url_for('admin'))


@app.route("/logout")
def logout():
    session.pop('logged_in', None)
    flash('You were logged out.')
    return redirect(url_for('login'))


@app.route("/admin/dashboard")
def admin():
    return render_template("admin/admin.html")


@app.route('/admin/users')
def users():
    return render_template('admin/user/users.html')


@app.route('/admin/roles')
def roles():
    return render_template('admin/role/roles.html')


if __name__ == '__main__':
    app.run()