import logging
import tempfile
import os
import json
import requests
from fastapi import HTTPException, UploadFile
from .pinata import upload_to_pinata, download_from_pinata, unpin_from_pinata
from .encryption import encrypt_data, decrypt_data

logger = logging.getLogger(__name__)

async def store_data(file: UploadFile):
    try:
        # Read the file content
        content = await file.read()

        # Encrypt the data
        encrypted_data = encrypt_data(content)

        # Upload to Pinata
        ipfs_hash = upload_to_pinata(encrypted_data, file.filename)

        return {"success": True, "ipfs_hash": ipfs_hash}
    except Exception as e:
        logger.error(f"Error in store_data: {e}")
        raise HTTPException(status_code=500, detail=str(e))


async def retrieve_data(ipfs_hash: str):
    try:
        logger.info(f"Downloading from Pinata with IPFS hash: {ipfs_hash}")
        encrypted_data_json = download_from_pinata(ipfs_hash)
        if encrypted_data_json is None:
            raise ValueError("Failed to download data from Pinata")
        logger.info(f"Downloaded encrypted data: {encrypted_data_json}")
        
        # Convert the JSON data back to bytes for decryption
        encrypted_data = json.dumps(encrypted_data_json).encode('utf-8')
        
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(encrypted_data)
            temp_file_path = temp_file.name

        decrypted_data = decrypt_data(encrypted_data, temp_file_path)
        os.unlink(temp_file_path)  # Delete the temporary file
        
        logger.info(f"Decrypted data length: {len(decrypted_data)}")
        return {"success": True, "data": decrypted_data}
    except ValueError as ve:
        logger.error(f"Value error in retrieve_data: {str(ve)}")
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        logger.error(f"Error in retrieve_data: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

async def delete_data(ipfs_hash: str):
    try:
        logger.info(f"Unpinning from Pinata with IPFS hash: {ipfs_hash}")
        response = unpin_from_pinata(ipfs_hash)
        logger.info(f"Unpin response: {response}")
        
        if response['success']:
            return {"success": True, "message": response['message']}
        else:
            raise HTTPException(status_code=500, detail=f"Failed to unpin from Pinata: {response['error']}")
    except Exception as e:
        logger.error(f"Unexpected error in delete_data: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))