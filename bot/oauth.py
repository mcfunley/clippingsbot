from bot import team, monitor
import os
import sys
import flask
import requests
from urllib.parse import urlencode

slack_scope = 'chat:write:bot,commands'

def authorize_url():
    params = {
        'client_id': os.getenv('SLACK_CLIENT_ID'),
        'redirect_uri': os.getenv('CALLBACK_URL'),
        'scope': slack_scope,
        'state': flask.session['id'],
    }
    return 'https://slack.com/oauth/authorize?%s' % urlencode(params)

def callback():
    req = flask.request
    if flask.session['id'] != req.args.get('state'):
        monitor.notify('Session ID mismatch in oauth callback: %s != %s',
                       flask.session['id'], req.args.get('state'))
        return flask.redirect('/?ref=bad-oauth-state')

    if req.args.get('error') == 'access_denied':
        return flask.redirect('/?ref=oauth-denied')

    r = requests.get('https://slack.com/api/oauth.access', params={
        'code': req.args.get('code'),
        'redirect_uri': os.getenv('CALLBACK_URL'),
        'client_id': os.getenv('SLACK_CLIENT_ID'),
        'client_secret': os.getenv('SLACK_CLIENT_SECRET'),
    })

    if r.status_code != 200:
        return flask.redirect('/?ref=oauth-access-failed')

    data = r.json()
    if not data['ok']:
        vals = ','.join(['%s=%s' % (k, v) for k, v in data.items()])
        monitor.notify('oauth was not ok: %s' % vals)
        return flask.redirect('/?ref=oauth-access-not-ok')

    team.save(data)
    monitor.notify('Authorized team: %s (%s)' % (
        data['team_name'], data['team_id']))
    return flask.redirect('/installed?team-id=%s' % data['team_id'])
