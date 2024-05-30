from sqlalchemy import create_engine
import pandas as pd
import psycopg2
import pika
import datetime as dt
import time
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

db_url = 'postgresql://postgres:password@localhost:5432/postgres'
engine = None

try:
    engine = create_engine(db_url)
    logging.info("Database engine created successfully")
except Exception as e:
    logging.error(f"Error creating database engine: {e}")
    exit(1)  # Exit the program if the database connection fails

print(engine)

# Callback function to handle incoming messages
def callback(ch, method, properties, body):
    try:
        tm = dt.datetime.now()
        logging.info(f"[{tm}] Received {body}")
        data = json.loads(body)
        data = pd.DataFrame([data])
        logging.info(f"DataFrame created: {data}")
        data.to_sql(name='temp2_rabit', con=engine, if_exists='append', index=False)
        logging.info("Data inserted into database successfully")
    except json.JSONDecodeError as json_err:
        logging.error(f"Error decoding JSON: {json_err}")
    except pd.io.sql.DatabaseError as db_err:
        logging.error(f"Database error: {db_err}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")

try:
    # Connect to RabbitMQ server
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    logging.info("Connected to RabbitMQ server successfully")

    # Declare the queue
    channel.queue_declare(queue='hello')
    logging.info("Queue declared successfully")

    # Set up a consumer and specify the callback function
    channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)
    logging.info("Consumer set up successfully, waiting for messages")

    channel.start_consuming()
except pika.exceptions.AMQPConnectionError as conn_err:
    logging.error(f"Connection error with RabbitMQ: {conn_err}")
except pika.exceptions.ChannelError as chan_err:
    logging.error(f"Channel error with RabbitMQ: {chan_err}")
except KeyboardInterrupt:
    logging.info("Interrupt received, stopping consumer")
    try:
        if channel:
            channel.stop_consuming()
        if connection:
            connection.close()
        logging.info("RabbitMQ connection closed")
    except Exception as e:
        logging.error(f"Error closing RabbitMQ connection: {e}")
except Exception as e:
    logging.error(f"Unexpected error: {e}")
finally:
    if connection and not connection.is_closed:
        connection.close()
        logging.info("RabbitMQ connection closed in finally block")
