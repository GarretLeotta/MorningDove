#!/usr/bin/env python

import os

import pika

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
    channel.basic_publish(exchange='',
                        routing_key='hello',
                        body='Hello World!')
    print(" [x] Sent 'Hello World!'")
    connection.close()

if __name__ == '__main__':
    main()