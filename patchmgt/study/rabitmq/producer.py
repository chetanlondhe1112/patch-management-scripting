import pika
import datetime as dt
import time
# Connect to RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare a queue
channel.queue_declare(queue='hello')
channel.queue_declare(queue='chetan_hello')


# Publish a message
while 1:
    channel.basic_publish(exchange='', routing_key='hello', body='Hello, RabbitMQ!')
    tm=dt.datetime.today().now()
    print(f" [{tm}] Sent 'Hello, RabbitMQ!'")
    time.sleep(5)

# Close connection
#connection.close()