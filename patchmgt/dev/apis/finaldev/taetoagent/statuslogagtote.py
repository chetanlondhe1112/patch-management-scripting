import os
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
import aiofiles
from sqlalchemy import update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import create_engine,text


# Database connection parameters
DATABASE_URL = "postgresql://postgres:password@localhost/postgres"
engine = create_engine(DATABASE_URL)


app = FastAPI()

# Directory to save uploaded files
UPLOAD_DIRECTORY = "D:/data_files/"
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

@app.post("/uploadfile/")
async def upload_file(ClientID: str = Form(...), Status: str = Form() , file: UploadFile = File(...)):
    #try:
    file_location = os.path.join(UPLOAD_DIRECTORY, file.filename)

    # Save the uploaded file
    async with aiofiles.open(file_location, 'wb') as out_file:
        content = await file.read()
        await out_file.write(content)

    # Update the database with file details
    stmt ="UPDATE cr_data SET logfile = '{}', logfilepath = '{}',status='{}' WHERE clientid = '{}';".format(file.filename,file_location,Status,ClientID)
    print(stmt)
    with engine.connect() as conn:
        result = conn.execute(text(stmt))
        conn.commit()
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="ClientID not found")

    return {"ClientID": ClientID, "filename": file.filename, "file_path": file_location}

    #except SQLAlchemyError as e:
    #    raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    #except Exception as e:
    #    raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(upload_file, host="103.159.85.174", port=8443, log_level="info")