from bot import team, patterns
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
/clippingsbot watch foo bar
/clippingsbot stop foo bar
```
"""


def show_help():
    return flask.jsonify({
        'response_type': 'in_channel',
        'text': usage
    })


def watch(phrase):
    if not len(phrase):
        return 'Sorry, I need a phrase. Usage: `/clippingsbot watch <phrase>`.'

    if len(phrase) < 6:
        return 'Sorry, the phrase must be six or more characters.'

    team_id = flask.request.form.get('team_id', None)
    if not team_id:
        return 'Bad request', 400

    t = team.find(team_id)
    if not t:
        return 'Bad request', 400

    if team.count_patterns(t) >= 100:
        return 'Sorry, you can watch a maximum of 100 phrases.'

    pattern_id = patterns.save(phrase)
    team.watch(t, phrase, pattern_id)
    return "Ok, I'm watching for mentions of the phrase `%s`." % phrase


def stop(phrase):
    if not len(phrase):
        return 'Sorry, I need a phrase. Usage: `/clippingsbot stop <phrase>`'

    # todo

    return ('Ok, I will no longer notify you about '
            'mentions of the phrase `%s`.' % phrase)


def parse():
    cmd, *args = re.split('\s+', flask.request.form['text'].strip())
    return cmd.lower(), args


def list_patterns():
    team_id = flask.request.form.get('team_id', None)
    if not team_id:
        return 'Bad request', 400

    t = team.find(team_id)
    if not t:
        return 'Bad request', 400

    return 'I am watching for mentions of the following phrases: %s' % (
        ','.join(['`%s`' % p['display_pattern'] for p in team.find_patterns(t)]),
    )


def run():
    request = flask.request
    tok = os.getenv('SLACK_VERIFICATION_TOKEN')
    if request.form.get('token', None) != tok:
        return 'Forbidden', 403

    if not 'text' in request.form:
        return 'Bad request', 400

    cmd, args = parse()
    if cmd == 'help':
        return show_help()
    elif cmd == 'watch':
        return watch(' '.join(args))
    elif cmd == 'stop':
        return stop(' '.join(args))
    elif cmd == 'list':
        return list_patterns()

    return show_help()


# ***REMOVED***
