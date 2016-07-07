from app import app
import os
from flask import Flask
from flask import render_template
from wtforms import Form
#from flask.wtf import Form
from wtforms import IntegerField, BooleanField
from random import randint

from pylti.flask import lti

VERSION = '0.0.1'
app = Flask(__name__, static_url_path='/app/static')
app.config.from_object('config')


"""
class AddForm(Form):
    '''    
    Add data from Form

    :param Form:
    ''' 

    p1 = IntegerField('p1')
    p2 = IntegerField('p2')
    result = IntegerField('result')
    correct = BooleanField('correct')
"""
def error(exception=None):
    """ 
    render error page

    :param exception: optional exception
    :return: the error.html template rendered
    """
    return render_template('error.html')


@app.route('/is_up', methods=['GET'])
def hello_world():
    """ 
    Indicate the app is working. Provided for debugging purposes.

    :param lti: the `lti` object from `pylti`
    :return: simple page that indicates the request was processed by the lti
        provider
    """
    #return render_template('up.html', lti=lti)
    return "Hello, World!"



@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET'])
def index():
    """ 
    Return the demo index page
    """
    return app.send_static_file('index.html')

@app.route('/lti/', methods=['GET', 'POST'])
@lti(request='initial', error=error, app=app)
def lti_index(lti=lti):
    """ 
    initial access page to the lti provider.  
    This page provides authorization for the user and must be
    launced from an LTI consumer application.

    :param lti: the `lti` object from `pylti`
    :return: index page for lti provider
    """
    return render_template('lti_index.html', lti=lti)

@app.route('/rest', methods=['GET','POST', 'PUT', 'DELETE'])
def rest_index():
    """ 
    initial access page to the REST Demo.  
    :return: index page for the REST Demo

    """
    return render_template('rest_index.html', lti=lti)

def set_debugging():
    """ 
    enable debug logging

    """
    import logging
    import sys

    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(name)s - %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)

set_debugging()

if __name__ == '__main__':
    """
    For if you want to run the flask development server
    directly
    """
    port = int(os.environ.get("FLASK_LTI_PORT", 5000))
    host = os.environ.get("FLASK_LTI_HOST", "localhost")
    app.run(debug=True, host=host, port=port)
