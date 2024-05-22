from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Define the request body schema
class RequestBody(BaseModel):
    data: dict

# Create a FastAPI instance
app = FastAPI()

# Define the endpoint to receive JSON queries
@app.post("/receive_data/")
async def receive_data(request_body: RequestBody):
    received_data = request_body.data
    print("Received Data:", received_data)
    return {"message": "Data received successfully"}

# Run the FastAPI application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)