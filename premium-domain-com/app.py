import os
import socket

from flask import Flask
from flask import render_template
from flask import make_response
from flask import request

app = Flask(__name__)


@app.route('/')
def hello():
    hostname = socket.gethostname()
    return render_template('index.html', provider=hostname)


@app.route('/cookie')
def cookie():
    response = make_response(render_template('redirect.html'))
    response.set_cookie('big8', 'SUPER_SECRET')
    return response

@app.route('/protected')
def protected():
    big8value = request.cookies.get('big8')

    if big8value is None:
        return render_template('redirect.html')
    else:
        return render_template('protected.html', connected=True)

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port)
