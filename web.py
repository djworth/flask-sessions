import os
from flask import Flask, render_template, session

from sessions import RedisSessionBackend

app = Flask(__name__)
app.session_interface = RedisSessionBackend()
app.secret_key = 'bf171716eff34154b16d012d7c293663'

@app.route("/")
def hello():
    #session['name'] = 'Dan Worth'
    return 'Hello, %s' % session['name']

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.debug = True
    app.run(host='0.0.0.0', port=port)

