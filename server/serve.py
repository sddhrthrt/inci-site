from flask import Flask
from flask import request, url_for, redirect, jsonify
from flask import render_template
from wtforms import Form, BooleanField, StringField, validators, PasswordField
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager, current_user, login_user, logout_user
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

import logging
logging.basicConfig(filename="/var/tmp/inci-site/log.log", level = logging.DEBUG)

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] =     'mysql://root:root@localhost/enginee8_inci_site'
db = SQLAlchemy(app)
migrate = Migrate(app,db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

login_manager = LoginManager()
login_manager.init_app(app)
app.secret_key = "Thisisaverysecretkey"

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(25), unique = True)
    email = db.Column(db.String(64), unique = True)
    fb_username = db.Column(db.String(64), unique = True)
    password = db.Column(db.String(128))
    registrations = db.relationship('Registration', backref='user', lazy='dynamic')
    
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return "<User#%r: %r>"%(self.id, self.username)

class Registration(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return "<Regitsration#%r: %r>"%(self.id, self.user_id)


@login_manager.user_loader
def load_user(userid):
    user = User.query.filter_by(id=userid).first()
    if user:
        return user
    return None

class RegistrationForm(Form):
    username = StringField("username", [
        validators.Length(min=4, max=25), 
        validators.Required()
        ])
    email = StringField("email", [
        validators.Length(min=6, max=64),
        validators.Required()
        ])
    fb_username = StringField("facebook username", [validators.Length(max=64)])
    password =  PasswordField('password', [
        validators.Required(),
        validators.EqualTo('confirm', message="passwords must match")
        ])
    confirm = PasswordField('repeat password', [validators.Required()])

class LoginForm(Form):
    username = StringField("username", [
        validators.Length(min=4, max=25), 
        validators.Required()
        ])
    password =  PasswordField('password', [
        validators.Required(),
        ])

@app.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated():
        return jsonify(url=url_for('logout'))
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        logging.debug('reg %s, %s'%(form.username.data, form.email.data))
        user = User(username=form.username.data,
                    email = form.email.data,
                    password = form.password.data,
                    fb_username = form.fb_username.data)
        db.session.add(user)
        db.session.commit()
        return jsonify(url=url_for('login'))
    return render_template('register.html', form=form, submit_url = url_for('register'))


@app.route('/login', methods=["POST", "GET"])
def login():
    if current_user.is_authenticated():
        return jsonify(url=url_for('index'))
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        logging.debug("got %s, %s"%(form.username.data, form.password.data))
        user = User.query.filter_by(username = form.username.data).first()
        if user:
            if user.password == form.password.data:
                logging.debug("logging in "+form.username.data)
                login_user(user)
                logging.debug("redirecting to " + url_for('index'))
                return jsonify(url=url_for('index'))
            else: 
                logging.debug("username and password dont match: %s - %s (expected %s)"%(form.username.data,form.password.data, user.password))
        else: 
            logging.debug("user not found: "+form.username.data)
    return render_template('login.html', form=form, submit_url = url_for('login'))

@app.route('/')
def index():
    return render_template('index.html', user=current_user)

@app.route('/logout')
def logout():
    if current_user.is_authenticated():
        logout_user()
    return redirect(url_for('login'))

if __name__=='__main__':
    app.debug = True
    manager.run()


