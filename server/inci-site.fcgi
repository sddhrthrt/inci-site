#!/home/sddhrthrt/inci-site-venv/bin/python

from flup.server.fcgi import WSGIServer
from serve import app as application

WSGIServer(application).run()

