import os
from pydantic import BaseModel
import pandas as pd
import psycopg2
import toml
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
import aiofiles
import logging
import json
import pika
from datetime import date

# deteime object json encoder
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, date):
            return obj.isoformat()
        return json.JSONEncoder.default(self, obj)

# Define the request body schema
class DeviceInfo(BaseModel):
    DeviceHostname: str
    DeviceIPAddress: str

# Define the response body schema
class ScheduleData(BaseModel):
    CRId: str
    StartDateTime: str
    EndDateTime: str
    ConfigurationFile: str

# Create a FastAPI instance
app = FastAPI()

# Load configuration from file
def load_config(config_file='taetoagent_config.toml'):
    """
        Method to read the configuration file
    """
    return toml.load(config_file)

config = load_config()

# Database, API, Rabit, Status log file configuration
pg_config = config['database']
api_config = config['api']
rabbitmq_config = config['rabbitmq']
status_log_config = config['status_log_path']
api_log_path = config['api_log_path']

# Directory to save uploaded files
UPLOAD_DIRECTORY = status_log_config['path']
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

# Configure logging
get_schedule_data_log_path = api_log_path['get_schedule_path']
status_log_path = api_log_path['status_log_path']

@app.post("/get_schedule_data/", response_model=ScheduleData)
async def get_schedule_data(device_info: DeviceInfo):

    """
        Api to get the scheduled ata from SCB database from TAE
    """

    logging.basicConfig(filename=get_schedule_data_log_path,level=logging.INFO,format='%(asctime)s - %(levelname)s - %(message)s',)

    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(f"postgresql://{pg_config['username']}:{pg_config['password']}@{pg_config['host']}/{pg_config['database']}")
        
        # Query the database using pandas
        query = f"""
            SELECT *
            FROM cr_data
            WHERE vm_id = '{device_info.DeviceHostname}'
                AND vm_address = '{device_info.DeviceIPAddress}'
        """
        df = pd.read_sql(query, conn)
        # Close the connection
        conn.close()

        if df.empty:
            logging.error(f"ScheduleData not found")
            raise HTTPException(status_code=404, detail="ScheduleData not found")

        # Extract data from the DataFrame
        response_data = df.iloc[0].to_dict()

        return ScheduleData(
            CRId=response_data["cr_id"],
            StartDateTime=response_data["start_datetime"].strftime("%d-%m-%Y %H:%M"),
            EndDateTime=response_data["end_datetime"].strftime("%d-%m-%Y %H:%M"),
            ConfigurationFile=json.dumps(response_data, cls=CustomJSONEncoder)
        )
    except psycopg2.Error as e:
        logging.error(f"Database error: {str(e)}")
    except Exception as e:
        logging.error(f"Unexpected Error")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload_status_data/")
async def upload_file(ClientID: str = Form(...), Status: str = Form(), file: UploadFile = File(...)):

    """
        Api to Upload status log from agent to tae and then to rabitmq scb producer
    """
    logging.basicConfig(filename=status_log_path,level=logging.INFO,format='%(asctime)s - %(levelname)s - %(message)s',)

    try:

        conn = psycopg2.connect(f"postgresql://{pg_config['username']}:{pg_config['password']}@{pg_config['host']}/{pg_config['database']}")

        # Save the uploaded file
        file_location = os.path.join(UPLOAD_DIRECTORY, file.filename)
        async with aiofiles.open(file_location, 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)
        
        logging.info(f"File {file.filename} saved to {file_location}")

        # Update the database with file details
        stmt ="UPDATE cr_data SET logfile = '{}', logfilepath = '{}',status='{}' WHERE clientid = '{}';".format(file.filename,file_location,Status,ClientID)
        with conn.cursor() as cur:
            cur.execute(stmt)
            conn.commit()
            if cur.rowcount == 0:
                logging.error(f"ClientID : {ClientID} not found")
                raise HTTPException(status_code=404, detail="ClientID not found")

        logging.info(f"Database updated for ClientID {ClientID} with file {file.filename}")

        # Prepare the message to send to RabbitMQ
        message = {
            "ClientID": ClientID,
            "Status": Status,
            "filename": file.filename,
            "file_path": file_location,
            "file_content": content.decode('utf-8')  # Assuming the file is a text file (e.g., CSV)
        }
        message_json = json.dumps(message)

        # Send the message to RabbitMQ
        connection = pika.BlockingConnection(pika.ConnectionParameters(
                        host=rabbitmq_config['host'],
                        port=rabbitmq_config['port']
                        ))
        
        channel = connection.channel()
        channel.queue_declare(queue=rabbitmq_config['queue'])
        channel.basic_publish(exchange='', routing_key=rabbitmq_config['routing_key'], body=message_json)
        connection.close()

        logging.info(f"Message sent to RabbitMQ: {message_json}")

        return {"ClientID": ClientID, "filename": file.filename, "file_path": file_location}

    except psycopg2.Error as e:
        logging.error(f"Database error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except pika.exceptions.AMQPError as e:
        logging.error(f"RabbitMQ error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"RabbitMQ error: {str(e)}")
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=api_config['host'], port=api_config['port'], log_level="info")