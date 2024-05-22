import pika
import json
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pandas as pd

# RabbitMQ connection parameters
rabbitmq_params = {
    'host': 'localhost',
    'port': 5672,
    'username': 'guest',
    'password': 'guest',
    'queue': 'your_queue_name',
}

# PostgreSQL connection parameters
postgresql_params = {
    'host': 'localhost',
    'port': 5432,
    'database': 'your_database_name',
    'user': 'your_database_user',
    'password': 'your_database_password',
}

# Define SQLAlchemy model
Base = declarative_base()

class YourModel(Base):
    __tablename__ = 'your_table_name'
    id = Column(Integer, primary_key=True)
    column1 = Column(String)
    column2 = Column(String)

# Connect to PostgreSQL database
engine = create_engine(f"postgresql://{postgresql_params['user']}:{postgresql_params['password']}@{postgresql_params['host']}:{postgresql_params['port']}/{postgresql_params['database']}")
Session = sessionmaker(bind=engine)

# Callback function to process messages from RabbitMQ
def callback(ch, method, properties, body):
    message = body.decode('utf-8')

    try:
        # Load JSON data
        data = json.loads(message)

        # Create pandas DataFrame
        df = pd.DataFrame(data, index=[0])

        # Connect to PostgreSQL and store data using SQLAlchemy ORM
        session = Session()
        session.bulk_insert_mappings(YourModel, df.to_dict(orient='records'))
        session.commit()
        session.close()
        
        print("Data saved successfully:", data)
    except Exception as e:
        print("Error:", e)

# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host=rabbitmq_params['host'],
    port=rabbitmq_params['port'],
    credentials=pika.PlainCredentials(rabbitmq_params['username'], rabbitmq_params['password'])
))
channel = connection.channel()

# Declare the queue
channel.queue_declare(queue=rabbitmq_params['queue'])

# Set up a consumer to receive messages from RabbitMQ
channel.basic_consume(queue=rabbitmq_params['queue'], on_message_callback=callback, auto_ack=True)

print('Waiting for messages...')
channel.start_consuming()