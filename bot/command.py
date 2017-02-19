from bot import team
import flask
import os
import re

usage = """Usage: `/clippingsbot [command] [arguments]`

Commands:

`help`     Display this help.
`watch`    Watch for mentions of a phrase.
`stop`     Stop watching for mentions of a phrase.
`list`     List phrases currently being watched.

Examples:

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

    # todo
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
        # todo
        pass

    return show_help()


# ***REMOVED***
