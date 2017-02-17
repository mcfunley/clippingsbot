# clippingsbot

## Dev setup

```
brew install flyway pyenv pyenv-virtualenv postgresql

pyenv virtualenv 3.6.0 clippingsbot
pyenv activate clippingsbot
pip install -r requirements.txt

createdb clippingsbot
bin/migrate
```

Make an `env.yaml` file, and put environment variables in it. (You can grep the codebase for `os.getenv` or look at the env settings in Skyliner to get a current list of the ones you need.)

Running the dev server:

```
./dev.py run
```

Getting a dev repl:

```
python -i dev.py
```
