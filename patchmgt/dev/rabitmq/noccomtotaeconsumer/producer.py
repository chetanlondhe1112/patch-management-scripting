from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pika
import json

app = FastAPI()

# Pydantic model for the JSON data
class Message(BaseModel):
    cr_id: str
    start_datetime: str
    end_datetime: str
    configuration_file: str
    vm_id: str
    vm_address: str
    logfile: str
    status: str
    logfilepath: str 
    clientid: str
    tool_name: str
    host_name: str
    agent_exe_name: str
    service_display_name: str
    agent_location: str 
    patch_download_path: str 

@app.post("/send/")
async def send_message(message: Message):
    try:
        # Connect to RabbitMQ server
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()

        # Declare a queue
        channel.queue_declare(queue='hello')

        # Convert message to JSON string
        message_json = message.json()

        # Send message to the queue
        channel.basic_publish(exchange='', routing_key='hello', body=message_json)

        # Close the connection
        connection.close()

        return {"status": "Message sent successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))