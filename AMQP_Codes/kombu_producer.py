from kombu import Connection, Exchange, Producer, Queue, message as msgs
import time
import json
import random

'''
Sample producer code for RabbitMQ using kombu library

'''

def data_publish(connection, channel):
    exchange = Exchange('data_exchange', type="direct")
    producer = Producer(exchange=exchange, channel=channel, routing_key='data_info')
    queue = Queue(name="data_q", exchange=exchange, routing_key="data_info", queue_arguments={
        'x-ha-policy': 'all'

    })
    queue.maybe_bind(connection)
    queue.declare()
    message = ['{"device_id": "30c15b59-650a-42a7", "check": false}',
               '{ "device_id": "30c15b59-650a-42a7", "check": true}',
               '{ "device_id": "30c15b59-650a-42a7", "check": true}',
               '{"device_id": "30c15b59-650a-42a7", "check": false}',
               '{"device_id": "30c15b59-650a-42a7", "check": true}'
               ]

    for msg in message:
        producer.publish(msg)
        print "Message published", msg
        time.sleep(2)

if __name__ == '__main__':
    rabbit_url = "amqp://{server_ip}:5672/"
    connection = Connection(rabbit_url)
    channel = connection.channel()
    while(True):
        data_publish(connection,channel)
