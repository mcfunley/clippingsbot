from bot import team, patterns, monitor
import flask
import os
import re

usage = """*Usage*:
`/clippingsbot [command] [arguments]`

*Commands*:
```
help      Display this help.
watch     Watch for mentions of a phrase.
stop      Stop watching for mentions of a phrase.
list      List phrases currently being watched.
feedback  Send feedback or bug reports about clippingsbot.
```

*Examples*:
```
/clippingsbot watch foobar.com
/clippingsbot watch several words
/clippingsbot stop foobar.com
```
"""


def show_help():
    return flask.jsonify({
        'response_type': 'in_channel',
        'text': usage
    })


def notify(msg):
    monitor.notify('%s (user=%s, team=%s (%s)' % (
        msg,
        flask.request.form.get('user_name', None),
        flask.request.form.get('team_domain', None),
        flask.request.form.get('team_id', None),
    ))


def watch(phrase):
    if not len(phrase):
        return 'Sorry, I need a phrase. Usage: `/clippingsbot watch <phrase>`.'

    if len(phrase) < 4:
        return 'Sorry, the phrase must be four or more characters.'

    team_id = flask.request.form.get('team_id', None)
    if not team_id:
        return 'Bad request', 400

    channel_id = flask.request.form.get('channel_id', None)
    if not channel_id:
        return 'Bad request', 400

    t = team.find(team_id)
    if not t:
        return 'Bad request', 400

    if team.count_patterns(t) >= 100:
        notify('too many patterns')
        return 'Sorry, you can watch a maximum of 100 phrases.'

    pattern_id = patterns.save(phrase)
    team.watch(t, channel_id, phrase, pattern_id)
    notify('watched a phrase')
    return ("Ok, I'm watching for mentions of the phrase `%s` "
            "in this channel." % phrase)


def stop(phrase):
    if not len(phrase):
        return 'Sorry, I need a phrase. Usage: `/clippingsbot watch <phrase>`.'

    team_id = flask.request.form.get('team_id', None)
    if not team_id:
        return 'Bad request', 400

    channel_id = flask.request.form.get('channel_id', None)
    if not channel_id:
        return 'Bad request', 400

    t = team.find(team_id)
    if not t:
        return 'Bad request', 400

    team.stop(t, channel_id, phrase)
    notify('stopped watching a phrase')
    return ("Ok, I won't alert you about mentions of `%s` "
            "in this channel." % phrase)


def parse():
    cmd, *args = re.split('\s+', flask.request.form['text'].strip())
    return cmd.lower(), args


def list_patterns():
    team_id = flask.request.form.get('team_id', None)
    if not team_id:
        return 'Bad request', 400

    channel_id = flask.request.form.get('channel_id', None)
    if not channel_id:
        return 'Bad request', 400

    t = team.find(team_id)
    if not t:
        return 'Bad request', 400

    channel_id = flask.request.form.get('channel_id', None)
    if not channel_id:
        return 'Bad request', 400

    channel_watches = list(team.find_patterns(t, channel_id))
    other_channels_count = team.count_other_channel_patterns(t, channel_id)

    notify('listed patterns')

    if other_channels_count > 0:
        if other_channels_count > 1:
            other_channels_msg = ('I am watching for %s phrases in other '
                                  'channels.' % other_channels_count)
        else:
            other_channels_msg = ('I am watching for one phrase in '
                                  'another channel.')

    if not len(channel_watches):
        if other_channels_count == 0:
            return 'I am not currently watching for any phrases.'
        else:
            return other_channels_msg

    phrase_list = ','.join(['`%s`' % p['display_pattern']
                            for p in channel_watches])
    msg = ('I am watching for mentions of the following phrases '
           'in this channel: %s.' % phrase_list)
    if other_channels_count == 0:
        return msg

    return '%s %s' % (msg, other_channels_msg)


def feedback(args):
    pass


def run():
    request = flask.request
    tok = os.getenv('SLACK_VERIFICATION_TOKEN')
    if request.form.get('token', None) != tok:
        return 'Forbidden', 403

    if not 'text' in request.form:
        return 'Bad request', 400

    cmd, args = parse()
    if cmd == 'help':
        notify('showed help')
        return show_help()
    elif cmd == 'watch':
        return watch(' '.join(args))
    elif cmd == 'stop':
        return stop(' '.join(args))
    elif cmd == 'list':
        return list_patterns()
    elif cmd == 'feedback':
        return feedback(' '.join(args))

    notify('unknown command')
    return show_help()
