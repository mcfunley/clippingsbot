# Clippingsbot

Clippingsbot is a Slack bot that watches Hacker News submissions for mentions of words and phrases.

Clippingsbot is a project of [Skyliner](https://www.skyliner.io), a deployment platform for AWS. You can use Skyliner to build your own Slack bot like this one.

## Architecture

The Slack command endpoint is a simple flask app. End users of the bot run `/clippingsbot <command>` in their slack, and that is routed by `bot/app.py` to one of the implementations in `bot/commands.py`.

There is also a worker process (in `bot/worker.py`). The worker does two things:

* It crawls for new mentions of watched phrases.
* It sends notifications to end users.

The two stages of notification are separated. Mentions found when crawling are stored in an RDS postgres database, and then picked up and turned into notifications in a second pass.

The worker and the web app are run together in a single Docker container using [supervisor](http://supervisord.org/). This is done since they share code, and therefore should have a single deploy button.

Clippingsbot uses [Cloudwatch Events](http://docs.aws.amazon.com/AmazonCloudWatch/latest/events/WhatIsCloudWatchEvents.html) combined with [SQS](https://aws.amazon.com/sqs/) to run scheduled jobs (i.e., a distributed cron). An event enqueues work in SQS, and the worker process loops in an endless SQS poll dequeueing and dispatching it.

## Dev setup

```
brew install flyway pyenv pyenv-virtualenv postgresql yarn nodejs

pyenv virtualenv 3.6.0 clippingsbot
pyenv activate clippingsbot
pip install -r requirements.txt

yarn install
yarn global add gulp-cli

createdb clippingsbot
bin/migrate
```

Make a `.env` file, and put environment variables in it (`X="Y"` syntax). You can grep the codebase for `os.getenv` or look at the env settings in Skyliner to get a current list of the ones you need.

Running the dev server:

```
bin/dev
```

Also run the frontend (in a different console):

```
gulp build && gulp watch
```

To get a dev repl:

```
bin/repl
```

### Tests

To run the tests:

```
python -m unittest -v test
```

### Coding

Slack doesn't have a great way, short of creating multiple bots, to develop a bot that's already in production. For now, you can do most things from the repl.

```
$ bin/repl
>>> from bot import crawl
>>> crawl.run()

>>> from bot import notify
>>> notify.run()
```


## AWS Credentials

**Do not write code that refers to `AWS_SECRET_ACCESS_KEY` and `AWS_ACCESS_KEY_ID`**.

Use [credentials files](http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html#cli-config-files). The `AWS_PROFILE` env var with [named profiles](http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html#cli-multiple-profiles) is handy if you are juggling multiple accounts.
