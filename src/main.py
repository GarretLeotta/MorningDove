#!/usr/bin/env python

import os

import pika

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

def callback(ch, method, properties, body):
    print(f" [x] Received {body}")

def main():
    print(get_params())
    connection = pika.BlockingConnection(get_params())
    channel = connection.channel()
    channel.queue_declare(queue='hello')
    channel.basic_consume(queue='hello',
                      auto_ack=True,
                      on_message_callback=callback)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    main()