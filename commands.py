#!/usr/bin/env python3
from flask import Flask, render_template, request, jsonify
import os
import requests

app = Flask('slack-command-flask')

def random_wikipedia_article():
    resp = requests.get('https://en.wikipedia.org/wiki/Special:Random',
                        allow_redirects=False)
    return resp.headers['Location']

@app.route('/commands/demo', methods=['POST'])
def demo():
    if request.form.get('token') != os.getenv('SLACK_COMMAND_TOKEN'):
        #return 'Unauthorized', 401
        pass

    return jsonify({
        'response_type': 'in_channel',
        'text': ('It works! Here is a random Wikipedia article: %s' %
                 random_wikipedia_article()),
    })

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run('localhost')
