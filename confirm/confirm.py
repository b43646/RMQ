# -*- coding: utf-8 -*-
# pylint: disable=C0111,C0103,R0205,W0603
import pika
from pika import spec

ITERATIONS = 100

confirmed = 0
errors = 0
published = 0


def on_open(conn):
    conn.channel(on_open_callback=on_channel_open)


def on_channel_open(channel):
    global published
    channel.confirm_delivery(ack_nack_callback=on_delivery_confirmation)
    for _iteration in range(0, ITERATIONS):
        channel.basic_publish(
            'hello-exchange', 'hola', 'message body value',
            pika.BasicProperties(content_type='text/plain', delivery_mode=2))
        published += 1


def on_delivery_confirmation(frame):
    global confirmed, errors
    if isinstance(frame.method, spec.Basic.Ack):
        confirmed += 1
        print("ACK")
    else:
        errors += 1
        print("NACK")
    if (confirmed + errors) == ITERATIONS:
        print('All confirmations received, published %i, confirmed %i with %i errors' % (published, confirmed, errors))
        connection.close()


parameters = pika.URLParameters(
    'amqp://guest:guest@192.168.1.32:5672/%2F?connection_attempts=50')
connection = pika.SelectConnection(
    parameters=parameters, on_open_callback=on_open)

try:
    connection.ioloop.start()
except KeyboardInterrupt:
    connection.close()
    connection.ioloop.start()
