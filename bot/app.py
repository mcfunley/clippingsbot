#!/usr/bin/env python3
from flask import Flask, render_template, request, jsonify
import os
import requests

app = Flask('clippingsbot')

@app.route('/command', methods=['POST'])
def command():
    if request.form.get('token') != os.getenv('SLACK_COMMAND_TOKEN'):
        # TODO:
        # You should verify that the request is coming from your Slack
        # instance if you return anything more interesting than a Wikipedia
        # article about dogs.
        #
        # To find your token, visit the configuration page. Go to:
        # https://<your slack>.slack.com/apps/manage/custom-integrations
        #
        # Then choose Slash Commands > Edit configuration (for this command).
        # Save this token in your Skyliner environment variables for this app
        # as SLACK_COMMAND_TOKEN.
        #
        # You can then enable verification by uncommenting the following
        # line and removing the pass statement below it.
        #
        # return 'Unauthorized', 401
        pass

    return jsonify({
        'response_type': 'in_channel',
        'text': ('It works! Here is a random wiki about dogs: %s' %
                 random_wikipedia_article()),
    })

@app.route('/')
def index():
    return render_template('index.jinja')
