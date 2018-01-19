import json
import logging
from flask import Flask, g, redirect, render_template, url_for
from flask_oidc import OpenIDConnect

logging.basicConfig()

config = {'OIDC_CLIENT_SECRETS': './client_secrets.json',
          'OIDC_ID_TOKEN_COOKIE_SECURE': False,
          'OIDC_VALID_ISSUERS': 'http://localhost:8001/openid',
          'SECRET_KEY': 'web'}

oidc_overrides = {}

app = Flask(__name__)
app.config.update(config)
oidc = OpenIDConnect(app, **oidc_overrides)


# @app.route('/api')
# @oidc.accept_token()
# def my_api():
#     # return json.dumps('Welcome %s' % g.oidc_token_info['sub'])


@app.route('/')
def index():
    return render_template('index.html', oidc=oidc)
    # if oidc.user_loggedin:
    #     # return 'Welcome %s.<br/><br/><a href="/logout">Click here to log out</a>'
    # else:
    #     return 'Not logged in.</br><a href="/login">Click here to log in</a>'


@app.route('/login')
@oidc.require_login
def login():
    return redirect("/", code=302)


@app.route('/logout')
def logout():
    oidc.logout()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host="localhost", port=5000, debug=True)
