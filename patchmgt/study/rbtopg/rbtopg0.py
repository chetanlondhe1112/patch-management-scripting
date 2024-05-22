from sqlalchemy import create_engine
import pandas as pd
import psycopg2
import pika
import datetime as dt
import time
import json
# Connection string format: dialect+driver://username:password@host:port/database
# Replace 'postgresql://username:password@host:port/database' with your actual connection string
db_url = 'postgresql://postgres:password@localhost:5432/postgres'
engine = create_engine(db_url)

print(engine)

# Callback function to handle incoming messages

def callback(ch, method, properties, body):
    tm=dt.datetime.today().now()
    print(f" [{tm}] Received %r " % body)
    data=json.loads(body)
    data=pd.DataFrame([data])
    print(data)
    data.to_sql(name='temp2_rabit',con=engine,if_exists='append',index=0)

# Connect to RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare the queue
channel.queue_declare(queue='hello')

# Set up a consumer and specify the callback function
channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)
print(' [x] Waiting for messages. To exit, press CTRL+C')
channel.start_consuming()