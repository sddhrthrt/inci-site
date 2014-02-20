from flask import Flask
from flask import request, url_for, redirect
from flask import render_template
from wtforms import Form, BooleanField, StringField, validators
import logging
logging.basicConfig(filename="/var/tmp/inci-site/log.log", level = logging.DEBUG)

app = Flask(__name__)

class RegistrationForm(Form):
    username = StringField("username", [validators.Length(min=4, max=25)])
    email = StringField("email", [validators.Length(min=6, max=64)])
    

@app.route('/login', methods=["POST", "GET"])
def login():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        logging.debug("got %s, %s"%(form.username.data, form.email.data))
        logging.debug("redirecting to " + url_for('login'))
        redirect(url_for('login'))
    return render_template('login.html', form=form)


if __name__=='__main__':
    app.debug = True
    app.run('0.0.0.0')
