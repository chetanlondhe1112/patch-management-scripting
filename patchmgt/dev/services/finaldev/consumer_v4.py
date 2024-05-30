import pika
import datetime as dt
import json
import logging
import requests
import toml

# Configure logging
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load configuration from file
def load_config(config_file='F:\patch-managment-project-16\patch-management-scripting\patchmgt\dev\config\scb_config.toml'):
    return toml.load(config_file)

config = load_config()

# Callback function to handle incoming messages
def callback(ch, method, properties, body):
    try:
        tm = dt.datetime.now()
        logging.info(f"[{tm}] Received {body}")
        print(f"[{tm}] Received {body}")
        # Parse JSON data
        data = json.loads(body)
        
        # Send data to FastAPI endpoint
        response = requests.post("http://localhost:8002/insert/", json=data)
        
        if response.status_code == 200:
            print(f"Data sent to API successfully: {response.json()}")
            logging.info(f"Data sent to API successfully: {response.json()}")

        else:
            print(f"Data sent to API successfully: {response.json()}")
            logging.error(f"Failed to send data to API: {response.status_code} {response.text}")

    except json.JSONDecodeError as json_err:
        print(f"Error decoding JSON: {json_err}")
        logging.error(f"Error decoding JSON: {json_err}")

    except requests.RequestException as req_err:
        print(f"Error sending request to API: {req_err}")
        logging.error(f"Error sending request to API: {req_err}")

    except Exception as e:
        print(f"Unexpected error: {e}")
        logging.error(f"Unexpected error: {e}")

# RabbitMQ configuration
rabbitmq_config = config['rabbitmq']

try:
    # Connect to RabbitMQ server
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=rabbitmq_config['host'],
        port=rabbitmq_config['port']
    ))
    channel = connection.channel()
    logging.info("Connected to RabbitMQ server successfully")

    # Declare the queue
    channel.queue_declare(queue=rabbitmq_config['queue'])
    logging.info("Queue declared successfully")

    # Set up a consumer and specify the callback function
    channel.basic_consume(queue=rabbitmq_config['queue'], on_message_callback=callback, auto_ack=True)
    print("Consumer set up successfully, waiting for messages")
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