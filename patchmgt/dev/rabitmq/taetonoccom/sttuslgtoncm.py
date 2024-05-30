import os
import logging
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
import aiofiles
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import pika
import json
import toml

# Database connection parameters
DATABASE_URL = "postgresql://postgres:password@localhost/postgres"
engine = create_engine(DATABASE_URL)

app = FastAPI()

# Directory to save uploaded files
UPLOAD_DIRECTORY = "D:/data_files/"
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

# Configure logging
LOG_FILE = "app.log"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)

# Rabit MQ configuration
def load_config(config_file='config.toml'):
    return toml.load(config_file)

config = load_config()
rabbitmq_config = config['rabbitmq']

@app.post("/uploadfile/")
async def upload_file(ClientID: str = Form(...), Status: str = Form(), file: UploadFile = File(...)):
    try:
        # Save the uploaded file
        file_location = os.path.join(UPLOAD_DIRECTORY, file.filename)
        async with aiofiles.open(file_location, 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)
        
        logging.info(f"File {file.filename} saved to {file_location}")

        # Update the database with file details
        stmt = text("""
            UPDATE cr_data 
            SET logfile = :logfile, logfilepath = :logfilepath, status = :status 
            WHERE clientid = :clientid
        """)
        with engine.connect() as conn:
            result = conn.execute(stmt, {
                'logfile': file.filename,
                'logfilepath': file_location,
                'status': Status,
                'clientid': ClientID
            })
            conn.commit()
            if result.rowcount == 0:
                logging.error(f"ClientID {ClientID} not found")
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
        print(message_json)
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

    except SQLAlchemyError as e:
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
    uvicorn.run(app, host="127.0.0.1", port=8443, log_level="info")