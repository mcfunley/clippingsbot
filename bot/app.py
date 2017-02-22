#!/usr/bin/env python3
from bot import oauth, command
from flask import (
    Flask, render_template, request, jsonify, session, redirect,
    send_file, Response
)
import os
import requests
import uuid
from urllib.parse import urlparse, urlunparse
from werkzeug.contrib.fixers import ProxyFix

app = Flask('clippingsbot')
app.wsgi_app = ProxyFix(app.wsgi_app)
app.secret_key = os.getenv('SECRET_KEY')
app.config['TEMPLATES_AUTO_RELOAD'] = bool(
    os.getenv('TEMPLATES_AUTO_RELOAD', False))


@app.before_request
def set_session_id():
    if not session.get('id', None):
        session['id'] = str(uuid.uuid4())


def is_healthcheck():
    request_url = urlparse(request.url)
    return request_url.path == '/health'


@app.before_request
def redirect_canonical_host():
    canonical = os.getenv('CANONICAL_HOST', None)
    if not canonical:
        return

    if is_healthcheck():
        return

    u = list(urlparse(request.url))
    c = list(urlparse(canonical))
    if u[0:2] != c[0:2]:
        u[0:2] = c[0:2]
        return redirect(urlunparse(u), code=303)


@app.before_request
def force_basic_auth():
    user = os.getenv('BASIC_AUTH_USERNAME', None)
    pw = os.getenv('BASIC_AUTH_PASSWORD', None)

    if not user:
        return

    if is_healthcheck():
        return

    auth = request.authorization
    if not auth or not (auth.username == user and auth.password == pw):
        return Response(
            'Authorization required', 401, {
                'WWW-Authenticate': 'Basic realm="Login Required"'
            })


@app.route('/')
def index():
    return render_template('index.jinja', **{
        'authorize_url': oauth.authorize_url()
    })

@app.route('/health')
def health():
    return 'ok'

@app.route('/oauth')
def oauth_callback():
    return oauth.callback()

@app.route('/installed')
def installed():
    return render_template('installed.jinja')

@app.route('/command', methods=['POST'])
def cmd():
    return command.run()

@app.route('/favicon.ico', methods=['GET'])
def favicon():
    return send_file('static/favicon/favicon.ico', mimetype='image/x-icon')

@app.route('/help', methods=['GET'])
def help():
    return render_template('help.jinja')

@app.route('/privacy', methods=['GET'])
def privacy():
    return render_template('privacy.jinja')
