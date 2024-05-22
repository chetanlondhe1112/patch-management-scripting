import pika
import datetime as dt
import time
# Callback function to handle incoming messages

def callback(ch, method, properties, body):
    tm=dt.datetime.today().now()
    print(f" [{tm}] Received %r " % body)

# Connect to RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare the queue
channel.queue_declare(queue='hello')

# Set up a consumer and specify the callback function
channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)
print(' [x] Waiting for messages. To exit, press CTRL+C')
channel.start_consuming()