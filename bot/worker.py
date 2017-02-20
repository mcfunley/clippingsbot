from bot import crawl, notify
from boto import sqs
import json
import os


def run():
    conn = sqs.connect_to_region(os.getenv('SQS_REGION'))
    q = conn.get_queue(os.getenv('SQS_QUEUE'))

    while 1:
        for message in conn.receive_message(q, wait_time_seconds=5):
            data = json.loads(message.get_body())
            if data.get('message_type', None) == 'crawl':
                crawl.run()
            elif data.get('message_type', None) == 'notify':
                notify.run()

            conn.delete_message(q, message)
            print('Deleted message: %s' % message.get_body())


if __name__ == '__main__':
    run()
