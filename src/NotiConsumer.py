import asyncio
import functools
import json
import os

import pika

from clients.APNs import APNsClient

def sync(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.get_event_loop().run_until_complete(f(*args, **kwargs))
    return wrapper

def get_params():
    rabbitmq_host = os.environ.get('RABBITMQ_HOST', 'localhost')
    credentials = pika.PlainCredentials(
        os.environ.get('RABBITMQ_DEFAULT_USER', 'garret'),
        os.environ.get('RABBITMQ_DEFAULT_PASS', 'password'))
    return pika.ConnectionParameters(
        rabbitmq_host,
        int(os.environ.get('RABBITMQ_PORT', 5672)),
        '/',
        credentials)

class NotiConsumer(object):
    def __init__(self):
        self._client = APNsClient()
    
    @sync
    async def _msg_cb(self, ch, method, properties, body):
        msg = json.loads(body)
        print(f" [x] Received {msg}")
        await self._client.send_noti(msg['topic'], msg.get('type', 'alert'), msg['device'], msg['payload'], msg.get('expiry'), msg.get('priority'), msg.get('collapse'))

    def connect_rabbit(self):
        connection = pika.BlockingConnection(get_params())
        channel = connection.channel()
        channel.queue_declare(queue='hello')
        channel.basic_consume(queue='hello',
                        auto_ack=True,
                        on_message_callback=self._msg_cb)
        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()