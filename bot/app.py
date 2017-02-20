#!/usr/bin/env python3
from bot import oauth, command
from flask import Flask, render_template, request, jsonify, session, redirect
import os
import requests
import uuid
from urllib.parse import urlparse, urlunparse


app = Flask('clippingsbot')
app.secret_key = os.getenv('SECRET_KEY')
app.config['TEMPLATES_AUTO_RELOAD'] = bool(
    os.getenv('TEMPLATES_AUTO_RELOAD', False))


@app.before_request
def set_session_id():
    if not session.get('id', None):
        session['id'] = str(uuid.uuid4())


@app.before_request
def redirect_canonical_host():
    canonical = os.getenv('CANONICAL_HOST', None)
    if not canonical:
        return

    u = list(urlparse(request.url))
    c = list(urlparse(canonical))
    if u[0:2] != c[0:2]:
        u[0:2] = c[0:2]
        return redirect(urlunparse(u), code=303)


@app.route('/')
def index():
    return render_template('index.jinja', **{
        'authorize_url': oauth.authorize_url()
    })

@app.route('/oauth')
def oauth_callback():
    return oauth.callback()

@app.route('/installed')
def installed():
    return render_template('installed.jinja')

@app.route('/command', methods=['POST'])
def cmd():
    return command.run()
