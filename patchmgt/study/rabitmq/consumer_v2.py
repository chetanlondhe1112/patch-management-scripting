import pika

def process_logs(ch, method, properties, body):
    print("Received log message:", body.decode('utf-8'))

def process_events(ch, method, properties, body):
    print("Received event message:", body.decode('utf-8'))

# Connection parameters
connection_params = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(connection_params)
channel = connection.channel()

# Declare queues
channel.queue_declare(queue='logs_queue')
channel.queue_declare(queue='events_queue')

# Set up consumers
channel.basic_consume(queue='logs_queue', on_message_callback=process_logs, auto_ack=True)
channel.basic_consume(queue='events_queue', on_message_callback=process_events, auto_ack=True)

# Start consuming
print('Waiting for messages. To exit press CTRL+C')
channel.start_consuming()