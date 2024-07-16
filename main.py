import logging
from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
from src.data_manager import store_data, retrieve_data, delete_data
import uvicorn
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RetrieveRequest(BaseModel):
    ipfs_hash: str
    output_path: str

class IpfsHashRequest(BaseModel):
    ipfs_hash: str

app = FastAPI()

@app.post("/store")
async def store_data_endpoint(file: UploadFile = File(...)):
    try:
        result = await store_data(file)
        return result
    except Exception as e:
        logger.error(f"Error in store_data_endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/retrieve")
async def retrieve_data_endpoint(request: RetrieveRequest):
    try:
        result = await retrieve_data(request.ipfs_hash, request.output_path)
        return result
    except Exception as e:
        logger.error(f"Error in retrieve_data_endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/delete")
async def delete_data_endpoint(request: IpfsHashRequest):
    try:
        result = await delete_data(request.ipfs_hash)
        return result
    except Exception as e:
        logger.error(f"Error in delete_data_endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8002)