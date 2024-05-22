import pika

# Connection parameters
connection_params = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(connection_params)
channel = connection.channel()

# Declare exchanges
channel.exchange_declare(exchange='logs_exchange', exchange_type='direct')
channel.exchange_declare(exchange='events_exchange', exchange_type='direct')

# Declare queues
channel.queue_declare(queue='logs_queue')
channel.queue_declare(queue='events_queue')

# Bind queues to exchanges with routing keys
channel.queue_bind(exchange='logs_exchange', queue='logs_queue', routing_key='logs')
channel.queue_bind(exchange='events_exchange', queue='events_queue', routing_key='events')

# Publish some messages
channel.basic_publish(exchange='logs_exchange', routing_key='logs', body='Log message 4')
channel.basic_publish(exchange='events_exchange', routing_key='eventss', body='Event message 4')

print("Messages published.")

# Close connection
connection.close()