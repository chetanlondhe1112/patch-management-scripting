from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Define the request body schema
class RequestBody(BaseModel):
    query: dict

# Create a FastAPI instance
app = FastAPI()

# Define the endpoint to receive JSON queries
@app.post("/show_query/")
async def show_query(request_body: RequestBody):
    print(request_body.query)
    return request_body.query

# Run the FastAPI application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)