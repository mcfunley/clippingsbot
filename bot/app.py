#!/usr/bin/env python3
from bot import oauth
from flask import Flask, render_template, request, jsonify, session
import os
import requests
import uuid

app = Flask('clippingsbot')
app.secret_key = os.getenv('SECRET_KEY')


@app.before_request
def set_session_id():
    if not session.get('id', None):
        session['id'] = str(uuid.uuid4())


@app.route('/')
def index():
    return render_template('index.jinja', **{
        'authorize_url': oauth.authorize_url()
    })

@app.route('/oauth')
def oauth_callback():
    return oauth.callback()
