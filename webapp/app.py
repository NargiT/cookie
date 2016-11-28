import os

from flask import Flask
from flask import render_template
from flask import make_response
from flask import request
import json
import time

app = Flask(__name__)


@app.route('/')
def hello():
    hostname = os.environ['APP_ID']
    return render_template('index.html', hostname=hostname)


@app.route('/login/<string:username>')
def login(username):
    token = encryptToken(username)
    response = buildResponse(username, token)
    return response


def buildResponse(username, token):
    hostname = os.environ['APP_ID']
    response = make_response(render_template('redirect.html', username=username, hostname=hostname, token=token))
    response.set_cookie('big8', "{}:{}".format(username, time.time()))
    return response


def encryptToken(username):
    """

    :param username:
    :type username: str
    """
    return username[::-1].upper()


def decryptToken(token):
    """

    :param token:
    :type token: str
    """
    return token[::-1].lower()


@app.route('/cookie/<string:token>')
def cookie(token):
    hostname = os.environ['APP_ID']

    if isTokenValid(token):
        username = decryptToken(token)
        newToken = encryptToken(username)
        return buildResponse(username, newToken)
    else:
        return render_template('timeout.html', hostname=hostname)


def isTokenValid(token):
    return token.isupper()


@app.route('/protected')
def protected():
    hostname = os.environ['APP_ID']
    big8value = request.cookies.get('big8')

    if big8value is None:
        return render_template('timeout.html', hostname=hostname)
    else:
        return render_template('protected.html', connected=json.dumps(True), hostname=hostname)


@app.route('/logout')
def logout():
    hostname = os.environ['APP_ID']
    big8value = request.cookies.get('big8')

    if big8value is None:
        return render_template('logout.html', hostname=hostname)
    else:
        response = make_response(render_template('logout.html', hostname=hostname))
        response.set_cookie('big8', '', expires=0)
        return response


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port)
