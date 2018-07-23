from kombu import Connection, Exchange, Queue, Consumer

'''
Sample Kombu consumer to drain messages from AMQP message bus
'''
rabbit_url = "amqp://{rabbit_server_ip}:5672/"
conn = Connection(rabbit_url)
channel = conn.channel()


exchange = Exchange('data_exchange',type="direct")
queue = Queue(name="data_q", exchange=exchange, routing_key="data_info")

def process_message(body, message):
  print type(body) , body
  print type(message), message.body
  print("The body is {}".format(body))
  message.ack()

with Consumer(conn, queues=queue, callbacks=[process_message], accept=["text/plain","json"]):
  conn.drain_events(timeout=6000)
