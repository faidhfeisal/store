from fastapi import FastAPI, HTTPException
from storage.data_manager import store_data, retrieve_data, delete_data
import uvicorn

app = FastAPI()

@app.post("/store")
def store_data_endpoint(file_path: str):
    return store_data(file_path)

@app.post("/retrieve")
def retrieve_data_endpoint(ipfs_hash: str, output_path: str):
    return retrieve_data(ipfs_hash, output_path)

@app.post("/delete")
def delete_data_endpoint(ipfs_hash: str):
    return delete_data(ipfs_hash)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8001)
