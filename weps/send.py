#!/usr/bin/env python

import os
import json

import pika

#only for dev environment
if not os.environ.get('APNS_TOPIC'):
    from dotenv import load_dotenv
    load_dotenv()

payload = '{"aps":{"alert":{"title":"Notification Title","subtitle":"New Message","body":"Message Content"}},"navigation":"chat:1"}'

message = {
    "topic": os.environ.get('APNS_TOPIC', 'secret'),
    # "type": "alert",
    # "expiry": 0,
    # "priority": "5",
    # "collapse": "",
    "device": os.environ.get('TEST_DEVICETOKEN', 'secret'),
    "payload": payload,
}

def get_params():
    rabbitmq_host = 'localhost'
    credentials = pika.PlainCredentials(
        os.environ.get('RABBITMQ_DEFAULT_USER', 'garret'),
        os.environ.get('RABBITMQ_DEFAULT_PASS', 'password'))
    return pika.ConnectionParameters(
        rabbitmq_host,
        5672,
        '/',
        credentials)

def main():
    connection = pika.BlockingConnection(get_params())
    channel = connection.channel()
    channel.queue_declare(queue='hello')
    body = json.dumps(message)
    channel.basic_publish(exchange='',
                          routing_key='hello',
                          body=body)
    print(f" [x] Sent {body}")
    connection.close()

if __name__ == '__main__':
    main()