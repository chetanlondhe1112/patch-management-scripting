from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import psycopg2
import toml
from datetime import datetime

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
    return toml.load(config_file)

config = load_config()

# Database configuration
pg_config = config['database']

# API config
api_config = config['api']

# Database connection parameters
DATABASE_URL = "postgresql://postgres:password@localhost/postgres"

@app.post("/get_schedule_data/", response_model=ScheduleData)
async def get_schedule_data(device_info: DeviceInfo):
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(f"postgresql://{pg_config['username']}:{pg_config['password']}@{pg_config['host']}/{pg_config['database']}")
        
        # Query the database using pandas
        query = f"""
            SELECT cr_id, start_datetime, end_datetime, configuration_file
            FROM cr_data
            WHERE vm_id = '{device_info.DeviceHostname}'
              AND vm_address = '{device_info.DeviceIPAddress}'
        """
        df = pd.read_sql(query, conn)
        
        # Close the connection
        conn.close()

        if df.empty:
            raise HTTPException(status_code=404, detail="ScheduleData not found")

        # Extract data from the DataFrame
        response_data = df.iloc[0].to_dict()

        return ScheduleData(
            CRId=response_data["cr_id"],
            StartDateTime=response_data["start_datetime"].strftime("%d-%m-%Y %H:%M"),
            EndDateTime=response_data["end_datetime"].strftime("%d-%m-%Y %H:%M"),
            ConfigurationFile=response_data["configuration_file"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=str(api_config['host']), port=api_config['port'], log_level="info")