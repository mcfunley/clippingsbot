import os
import requests
from concurrent.futures import ThreadPoolExecutor


executor = ThreadPoolExecutor(max_workers=1)


def _notify(message):
    webhook_url = os.getenv('FEEDBACK_WEBHOOK_URL', None)
    if not webhook_url:
        return

    env_text = '' if os.getenv('ENV', '') == 'prod' else ' (TESTING)'

    requests.post(webhook_url, json={
        'text': '%s%s' % (message, env_text),
        'username': 'clippingsbot',
        'icon_url': 'https://www.clippingsbot.com/static/img/logo-120.png',
    })


def notify(message):
    executor.submit(_notify, message)
