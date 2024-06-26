from fastapi import FastAPI, HTTPException, Form
from sqlalchemy import update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import create_engine,text
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pydantic import BaseModel
import logging
import psycopg2

# Database connection parameters
DATABASE_URL = "postgresql://postgres:password@localhost/postgres"
conn = psycopg2.connect(DATABASE_URL)
cr=conn.cursor()

app = FastAPI()

# Pydantic model for the JSON data
class Data(BaseModel):
    cr_id: str
    start_datetime: str
    end_datetime: str
    configuration_file: str
    vm_id: str
    vm_address: str
    logfile: str
    status: str
    logfilepath: str = None
    clientid: str
    tool_name: str
    host_name: str
    agent_exe_name: str
    service_display_name: str
    agent_location: str = None
    patch_download_path: str = None

@app.post("/insert/")
async def insert_data(data: Data):
    try:
        # SQL Insert query
        insert_query = """
        INSERT INTO cr_data (
            cr_id, start_datetime, end_datetime, configuration_file,
            vm_id, vm_address, logfile, status, logfilepath, clientid,
            tool_name, host_name, agent_exe_name, service_display_name,
            agent_location, patch_download_path
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        ) RETURNING id;
        """

        # Execute the SQL query
        cr.execute(insert_query, (
            data.cr_id, data.start_datetime, data.end_datetime, data.configuration_file,
            data.vm_id, data.vm_address, data.logfile, data.status, data.logfilepath, data.clientid,
            data.tool_name, data.host_name, data.agent_exe_name, data.service_display_name,
            data.agent_location, data.patch_download_path
        ))
        conn.commit()

        # Fetch the id of the newly inserted row
        new_id = cr.fetchone()[0]
        logging.info(f"Inserted record with id: {new_id}")
        return {"status": "success", "id": new_id}
    except Exception as e:
        conn.rollback()
        logging.error(f"Error inserting data: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

