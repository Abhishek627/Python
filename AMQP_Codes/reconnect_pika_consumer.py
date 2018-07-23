import pika
import random
from retry import retry

'''
Sample code to randomly connect to different RabitMQ node in case of failure in current node. Uses retry decorator.
'''

def on_message(channel, method_frame, header_frame, body):
    print(method_frame.delivery_tag)
    print(body)
    print()
    channel.basic_ack(delivery_tag=method_frame.delivery_tag)

## Assuming there are three hosts: host1, host2, and host3
node1 = pika.URLParameters('pyamqp://{user}:{password}@10.204.249.81:5672/')
node2 = pika.URLParameters('pyamqp://{user}:{password}@10.204.249.82:5672/')
node3 = pika.URLParameters('pyamqp://{user}:{password}@10.204.249.83:5672/')
all_endpoints = [node1, node2, node3]

@retry(pika.exceptions.AMQPConnectionError, delay=5, jitter=(1, 3))
def consume():
    while True:
        random.shuffle(all_endpoints)
        endpoint= all_endpoints[0]
        print "connecting to endpoint", endpoint
        connection = pika.BlockingConnection(endpoint)
        channel = connection.channel()
        channel.basic_qos(prefetch_count=1)
        channel.queue_declare('recovery-example', durable = False, auto_delete = True)
        channel.basic_consume(consumer_callback=on_message,queue='recovery-example')

        try:
            channel.start_consuming()
        except KeyboardInterrupt:
            channel.stop_consuming()
            connection.close()
        except Exception as e:
            print "Exception occurred in connection. Connection broken"
            continue

consume()