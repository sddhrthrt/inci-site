from flask import Flask
from flask import request, url_for, redirect, jsonify, abort
from flask import render_template
from wtforms import Form, BooleanField, StringField, validators, PasswordField
from wtforms import FileField, FormField, DateField, HiddenField, IntegerField
from wtforms.validators import ValidationError
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager, current_user, login_user, logout_user, login_required
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
import os
import re
from werkzeug.utils import secure_filename
import logging
from random import randint
import logging
from flask_mail import Mail, Message
from datetime import datetime
import hashlib

app = Flask(__name__)
app.config.from_object('config')

logging.basicConfig(filename=app.config['LOG_FILE'], level = logging.DEBUG)
mail = Mail(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

login_manager = LoginManager()
login_manager.init_app(app)
app.secret_key = "Thisisaverysecretkey"

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(25), unique = True)
    email = db.Column(db.String(64), unique = True)
    fb_username = db.Column(db.String(64))
    password = db.Column(db.String(128))
    phone = db.Column(db.String(25))
    name = db.Column(db.String(64))
    college = db.Column(db.String(64))
    registrations = db.relationship('Registration', backref='user', lazy='dynamic')
    confirmations = db.relationship('Confirmation', backref='user', lazy='dynamic')

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

    def is_admin(self):
        role = Role.query.filter_by(user_id = self.id).first()
        if role:
            return role.role
        else:
            return "user"

class Role(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    role = db.Column(db.String(25))
    def __repr__(self):
        return "<Role#%r: %r>"%(self.id, self.role)

class Confirmation(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    hash_digest = db.Column(db.String(256))
    time = db.Column(db.DateTime())

    def __repr__(self):
        return "<confirmation#%r: %r>"%(self.id, self.user_id)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key  =True)
    name = db.Column(db.String(25), unique = True)
    details = db.Column(db.String(128))
    registrations = db.relationship('Registration', backref='event', lazy='dynamic')

    def __repr__(self):
        return "<Event#%r: %r>"%(self.id, self.name)

class DivaEntry(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    uid = db.Column(db.Integer, db.ForeignKey('user.id'))
    entry = db.Column(db.Text)

class Registration(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))

    def __repr__(self):
        return "<Regitsration#%r: %r for %r>"%(self.id, self.user_id, self.event_id)

class AddressForm(Form):
    address_s1 = StringField("Street Address", [
        validators.Length(max=128),
        validators.Required()
        ])
    address_s2 = StringField("Street Address 2", [
        validators.Length(max=128)
        ])
    city = StringField("City", [
        validators.Length(max=128),
        validators.Required()
        ])
    state = StringField("State/Province", [
        validators.Length(max=128),
        validators.Required()
        ])
    postal = StringField("Postal code", [
        validators.Length(max=12),
        validators.Required()
        ])
    country = StringField("Country", [
        validators.Length(max=32),
        validators.Required()
        ])

class DivaForm(Form):
    uid = HiddenField("uid")
    fname = StringField("First Name", [
        validators.Length(max=64),
        validators.Required()
        ])
    lname = StringField("Last name", [
        validators.Length(max=64),
        validators.Required()
        ])
    dob = DateField("DOB (dd-mm-yyyy)", [
        validators.Required()
        ], format="%d-%m-%Y")
    age = IntegerField("Age", [
        validators.Required()
        ])
    college = StringField("College Name", [
        validators.Length(max=128),
        validators.Required()
        ])
    address = FormField(AddressForm)
    contact = StringField("Contact Number", [
        validators.Length(max=32),
        validators.Required()
        ])
    email = StringField("Email", [
        validators.Length(max=32),
        validators.Required()
        ])
    height = StringField("Height in inches", [
        validators.Length(max=12),
        validators.Required()
        ])
    vitalstats = StringField("Vital Stats (36-24-36)", [
        validators.Length(max=32),
        validators.Required()
        ])


@login_manager.user_loader
def load_user(userid):
    user = User.query.filter_by(id=userid).first()
    if user:
        return user
    return None

class RegistrationForm(Form):
    name = StringField("Full Name", [
        validators.Length(min=4, max=64),
        validators.Required()
        ])

    email = StringField("Email", [
        validators.Length(min=6, max=64),
        validators.Required(),
        validators.Email()
        ])
    def validate_email(form, field):
        email = field.data
        user = User.query.filter_by(email=email).first()
        if user:
            raise ValidationError("Email ID used already")
    password =  PasswordField('Password', [
        validators.Required(),
        validators.EqualTo('confirm', message="passwords must match")
        ])
    confirm = PasswordField('Repeat Password', [validators.Required()])
    fb_username = StringField("Facebook Username", [validators.Length(max=64)])
    def validate_fb_username(form, field):
        fbu = field.data
        user = User.query.filter_by(fb_username=fbu).first()
        if user:
            raise ValidationError("Facebook ID used already")
    phone = StringField("Phone Number", [validators.Length(max=64), validators.Required()])
    college = StringField("College/University", [validators.Length(max=64), validators.Required()])


class LoginForm(Form):
    username = StringField("username/email", [
        validators.Length(min=4, max=64),
        validators.Required()
        ])
    password =  PasswordField('password', [
        validators.Required(),
        ])

class ResetPasswordRequestForm(Form):
    username = StringField("username/email", [
        validators.Length(min=4, max=64),
        validators.Required()
        ])

class ResetPasswordForm(Form):
    password =  PasswordField('Password', [
        validators.Required(),
        validators.EqualTo('confirm', message="passwords must match")
        ])
    confirm = PasswordField('Repeat Password', [validators.Required()])

def formatUsername(user):
    nameslug = user.name
    nameslug = re.sub("[\W]*", "", nameslug)
    nameslug = nameslug.upper()[:3]
    nameslug = "INCI14%s%s"%(nameslug, int(user.id))
    return nameslug

@app.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated():
        return jsonify(url=url_for('logout'))
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(
                    email = form.email.data,
                    password = form.password.data,
                    fb_username = form.fb_username.data,
                    phone = form.phone.data,
                    college = form.college.data,
                    name = form.name.data,
                    )
        db.session.add(user)
        db.session.commit()
        user.username = formatUsername(user)
        db.session.add(user)
        db.session.commit()
        return jsonify(url=url_for('login'))
    return render_template('register.html', form=form, submit_url = url_for('register'))

@app.route('/login', methods=["POST", "GET"])
def login():
    if current_user.is_authenticated():
        return jsonify(url=url_for('profile'))
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        logging.debug("got %s, %s"%(form.username.data, form.password.data))
        userbyname = User.query.filter_by(username = form.username.data).first()
        userbyemail = User.query.filter_by(email = form.username.data).first()
        user = userbyname or userbyemail
        if user:
            if user.password == form.password.data:
                logging.debug("logging in "+form.username.data)
                login_user(user)
                logging.debug("redirecting to " + url_for('index'))
                return jsonify(url=url_for('profile'))
            else:
                logging.debug("username and password dont match: %s - %s (expected %s)"%(form.username.data,form.password.data, user.password))
        else:
            logging.debug("user not found: "+form.username.data)
    return render_template('login.html', form=form, submit_url = url_for('login'), resetpasswordrequest_url = url_for('resetpasswordrequest'))

@app.route('/profiledata')
def profiledata():
    if current_user.is_authenticated():
        return render_template('profiledata.html', user=current_user, username=current_user.username, logout = url_for('logout'), resetpassword_url=url_for('resetpassword'))
    else:
        return redirect(url_for('profile'))

@app.route('/profile')
def profile():
    if current_user.is_authenticated():
        logging.debug("profiledata: "+url_for('profiledata'))
        return render_template('profile.html', user=current_user, logout=url_for('logout'), profiledata=url_for('profiledata'))
    else:
        return render_template('profile.html', user=None, login= url_for('login'), register = url_for('register'))


def allowed_file(filename):
    return '.' in filename and \
            filename.split('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

def save_form(form, filenames):
    keys = form.__dict__.keys()
    keys = filter(lambda a: not a.startswith("_"), keys)
    row = ''
    for i in keys:
        if not i=='address' and not i.startswith('photo'):
            data = getattr(form, i)
            if isinstance(data, int) or isinstance(data, long):
                row += i+":"+str(getattr(form, i))+","
            else:
                row += i+":"+str(getattr(form, i).data)+","
    for i in form.address.data.keys():
        row += "%s:%s,"%(i,form.address.data[i])
    row += filenames
    row = row.rstrip(",")+'\n'
    d = DivaEntry(uid=current_user.id, entry = row)
    db.session.add(d)
    db.session.commit()

@app.route('/diva', methods=["POST", "GET"])
def diva():
    if not current_user.is_authenticated():
        return render_template('diva.html', logged_in = False)
    form = DivaForm(request.form)
    form.uid = current_user.id
    photoerrors = ""
    if request.method == 'POST' and form.validate():
        filenames = ""
        for i in ('photo_full', 'photo_med', 'photo_close'):
            file_ = request.files[i]
            if file_ and allowed_file(file_.filename):
                filename = str(form.uid)+"_"+secure_filename(file_.filename)
                file_.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                filenames += "%s:%s,"%(i,filename)
            else:
                logging.debug("no file "+i)
                photoerrors += "All photos are compulsory"
        if not photoerrors:
            save_form(form, filenames)
            return render_template('diva_thanks.html')
    return render_template('diva.html', form=form, submit_url = url_for('diva'), logged_in = True, photoerrors = photoerrors)

@app.route('/')
def index():
    return render_template('index.html', user=current_user)

@app.route('/logout')
def logout():
    if current_user.is_authenticated():
        logout_user()
    return redirect(url_for('profile'))

@app.route('/preregister/<eventname>')
def preregister(eventname=None):
    """
    returns success / eventnotfound / login / alreadydone / invalid
    """
    logging.debug("registration for %s"%eventname)
    if current_user.is_authenticated():
        try:
            eventname = int(eventname)
        except:
            return jsonify({'response': 'invalid'})
        event = Event.query.filter_by(id=eventname).first()
        if event:
            already = Registration.query.filter_by(
                    user_id = current_user.id,
                    event_id = event.id).first()
            if already:
                return jsonify({'response': 'alreadydone'})
            registration = Registration(
                    user_id = current_user.id,
                    event_id = event.id)
            db.session.add(registration)
            db.session.commit()
            return jsonify({'response': 'success'})
        else:
            logging.error("event not found: %d"%eventname)
            return jsonify({'response': 'eventnotfound'})
    else:
        return jsonify({'response': 'login'})

@app.route('/adminpreregister', methods=["POST"])
def unpreregister():
    """
    returns successfullyadded / successfullyremoved / eventnotfound / login / alreadyadded / alreadyremoved / invalid
    """
    if current_user.is_authenticated() and current_user.is_admin():
        eventid = request.json['eventid']
        userid = request.json['userid']
        state = request.json['state']
        event = Event.query.filter_by(id=eventid).first()
        if event:
            already = Registration.query.filter_by(
                    user_id = userid,
                    event_id = event.id).first()
            if already:
                if not state:
                    db.session.delete(already)
                    db.session.commit()
                    return jsonify({'response': 'successfullyremoved'})
                return jsonify({'response': 'alreadyremoved'})
            else:
                if state:
                    registration = Registration(
                            user_id = current_user.id,
                            event_id = event.id)
                    db.session.add(registration)
                    db.session.commit()
                    return jsonify({'response': 'successfullyadded'})
                return jsonify({'response': 'alreadyadded'})
        else:
            logging.error("event not found: %d"%eventname)
            return jsonify({'response': 'eventnotfound'})
    else:
        return jsonify({'response': 'login'})


@app.route('/ispreregister/<eventname>')
def ispreregister(eventname=None):
    """
    returns eventnotfound / login / alreadydone / invalid / notregistered
    """
    logging.debug("registration for %s"%eventname)
    if current_user.is_authenticated():
        if eventname == "all":
            events = Event.query.all()
            regevents = [ e.event_id for e in Registration.query.filter_by(user_id = current_user.id).all() ]
            reply = {}
            for event in events:
                reply[event.id] = event.id in regevents
            return jsonify({'response': 'success',
                            'registrations': reply})
        try:
            eventname = int(eventname)
        except:
            return jsonify({'response': 'invalid'})
        event = Event.query.filter_by(id=eventname).first()
        if event:
            already = Registration.query.filter_by(
                    user_id = current_user.id,
                    event_id = event.id).first()
            if already:
                return jsonify({'response': 'alreadydone'})
            else:
                return jsonify({'response': 'notregistered'})
        else:
            logging.error("event not found: %d"%eventname)
            return jsonify({'response': 'eventnotfound'})
    else:
        return jsonify({'response': 'login'})

@app.route('/idforevent/<eventname>')
def idforevent(eventname = None):
    if eventname == "all":
        events = Event.query.all()
        reply = {}
        for e in events:
            reply[e.name] = e.id
        return jsonify({'response': 'success', 'eventids': reply})
    event = Event.query.filter_by(name=eventname).first()
    if event:
        return jsonify({'eventid': event.id, 'response': 'success'})
    else:
        return jsonify({'response': 'eventnotfound'})

@app.route('/randompic')
def randompic():
    return redirect('/images/loading%d.jpg'%(randint(1,3)))

def sendResetPasswordEmail(user, hash_digest):
    msg = Message("INCIDENT '14: Password Reset mailer",
            sender="siddhartha@incident.co.in",
            recipients=[user.email])
    msg.html = msg.body = render_template('resetpasswordmail.html', name=user.name,
            hash_digest = hash_digest)
    mail.send(msg)

@app.route('/resetpasswordrequest', methods=["POST", "GET"])
def resetpasswordrequest():
    form = ResetPasswordRequestForm(request.form)
    if request.method == 'POST' and form.validate():
        userbyusername = User.query.filter_by(username = form.username.data).first()
        userbyemail = User.query.filter_by(email = form.username.data).first()
        user = userbyusername or userbyemail
        if user:
            e = datetime.now()
            hash_digest = hashlib.md5(user.email+unicode(e)).hexdigest()
            confirmation = Confirmation(user_id = user.id,
                                        hash_digest = hash_digest,
                                        time = e)
            db.session.add(confirmation)
            db.session.commit()
            sendResetPasswordEmail(user, hash_digest)
            logging.debug("resetting: hash="+hash_digest)
            return redirect(url_for('login'))
        else:
            logging.debug("resetting: user not found")
            return render_template('resetpasswordrequest.html', form=None, submit_url=url_for('resetpasswordrequest'))
    return render_template('resetpasswordrequest.html', form=form, submit_url=url_for('resetpasswordrequest'))

@app.route('/resetpasswordreply/<hash_digest>')
def resetpasswordreply(hash_digest=None):
    confirmation = Confirmation.query.filter_by(hash_digest=hash_digest).first()
    if confirmation:
        logging.debug("confirmation present")
        user = confirmation.user
        logging.debug("logging in by hash: "+user.username)
        db.session.delete(confirmation)
        db.session.commit()
        login_user(user)
        return redirect(url_for('resetpassword'))
    logging.debug("no confirmation with hash"+hash_digest)
    return "Bad Request"

@app.route('/resetpassword', methods=["POST", "GET"])
def resetpassword():
    if current_user.is_authenticated():
        form = ResetPasswordForm(request.form)
        if request.method=="POST" and form.validate():
            user = current_user
            user.password = form.password.data
            db.session.add(user)
            db.session.commit()
            logging.debug("changed password: "+user.username)
            return redirect(url_for('profile'))
        logging.debug("changing password: User not found")
        return render_template('resetpassword.html', submit_url=url_for('resetpassword'), form=form)
    return render_template('resetpassword.html', notloggedin=True, form=form)

@app.route('/admin/home')
def admin():
    if current_user.is_authenticated() and current_user.is_admin():
        return render_template("admin.html", current_user = current_user)
    abort(404)

def objectAsDict(obj, keys):
    return dict((k, v) for k, v in obj.__dict__.iteritems() \
            if k in keys )

@app.route('/json/users', methods=["POST"])
def usersJson():
    if current_user.is_authenticated() and current_user.is_admin():
        users = User.query.all()
        keys = ['id', 'username', 'email', 'phone']
        userdicts = [ objectAsDict(u, keys) for u in users ]
        return jsonify({'users': userdicts})
    abort(404)

@app.route('/json/user/<uid>', methods=["POST"])
def usersJsonFromId(uid=None):
    if current_user.is_authenticated() and current_user.is_admin():
        if uid:
            keys = ['id', 'username', 'email', 'fb_username',
                    'phone', 'name', 'college' ]
            user = User.query.filter_by(id=uid).first()
            userdict = objectAsDict(user, keys)
            userdict.update(registrations = [ r.event_id for r in \
                    user.registrations.all() ])
            return jsonify(userdict)
    abort(404)

@app.route('/json/events', methods=["POST"])
def eventsJson():
    if current_user.is_authenticated() and current_user.is_admin():
        events = Event.query.all()
        keys = [ 'id', 'name', 'details' ]
        eventdicts = [ objectAsDict(e, keys) for e in events ]
        return jsonify({'events': eventdicts})
    abort(404)

@app.route('/json/event/<eid>', methods=["POST"])
def eventsJsonFromId(eid=None):
    if current_user.is_authenticated() and current_user.is_admin():
        if eid:
            keys = ['name', 'details']
            event = Event.query.filter_by(id=eid).first()
            eventdict = objectAsDict(event, keys)
            eventdict.update(registrations = [ r.user_id for r in \
                    event.registrations.all() ])
            return jsonify(eventdict)
    abort(404)


@app.route('/admin/mail')
def adminmail():
    if current_user.is_authenticated() and current_user.is_admin():
        events = Event.query.all()
        users = User.query.all()
        return render_template("adminmail.html", currentuser = current_user, events = events, users = users)
    abort(404)

@app.route('/admin/getparticipants', methods=["POST"])
def getParticipants():
    if current_user.is_authenticated() and current_user.is_admin():
        events = request.json['events']
        if events:
            checkedusers = set()
            registrations = Registration.query.filter(Registration.event_id.in_(events)).all()
            for r in registrations:
                checkedusers.add(r.user_id)
            return jsonify(checkedusers = list(checkedusers))
        else:
            return "no events";
    abort(404)

@app.route('/admin/sendemail', methods=["POST"])
def sendEmail():
    if current_user.is_authenticated() and current_user.is_admin():
        recipients = request.json['to']
        recipient_emails = [ u.email for u in User.query.filter(User.id.in_(recipients)).all() ]
        body = request.json['body']
        subject = request.json['subject']
        msg = Message(subject,
                sender="siddhartha@incident.co.in",
                recipients=recipient_emails)
        msg.html = msg.body = body
        try:
            mail.send(msg)
        except:
            return "failure"
        return "success"
    abort(404)


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = AddParticipantForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(
                    email = form.email.data,
                    password = hashlib.md5(form.email.data+form.name.data).hexdigest(),
                    fb_username = form.fb_username.data,
                    phone = form.phone.data,
                    college = form.college.data,
                    name = form.name.data,
                    )
        db.session.add(user)
        db.session.commit()
        user.username = formatUsername(user)
        db.session.add(user)
        db.session.commit()
        return jsonify(url=url_for('login'))
    return render_template('register.html', form=form, submit_url = url_for('register'))

if __name__=='__main__':
    app.debug = True
    manager.run()


