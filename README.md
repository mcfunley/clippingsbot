# clippingsbot

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

Also run the frontend:

```
gulp watch
```

To get a dev repl:

```
bin/repl
```

## AWS Credentials

**Do not write code that refers to `AWS_SECRET_ACCESS_KEY` and `AWS_ACCESS_KEY_ID`**.

Use [credentials files](http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html#cli-config-files). The `AWS_DEFAULT_PROFILE` env var with [named profiles](http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html#cli-multiple-profiles) is handy if you are juggling multiple accounts.
