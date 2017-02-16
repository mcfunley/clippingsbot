#!/usr/bin/env python3
from bot.app import app
import os
import sys
import yaml

if not os.path.exists('env.yaml'):
    print("Make an env.yaml file with environment variables for development.")
    sys.exit(1)

d = yaml.load(open('env.yaml', 'r').read())
for k, v in d.items():
    os.environ[k] = v

app.run('localhost')
