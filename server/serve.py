from flask import Flask
from flask import render_template
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('beach.html')

def room(): 
    return render_template('room.html')

if __name__=='__main__':
    app.debug = True
    app.run('0.0.0.0')
