import logging
import tempfile
import os
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

async def retrieve_data(ipfs_hash: str, output_path: str):
    try:
        logger.debug(f"Downloading from Pinata with IPFS hash: {ipfs_hash}")
        encrypted_data = download_from_pinata(ipfs_hash)
        logger.debug(f"Downloaded encrypted data length: {len(encrypted_data)}")
        decrypt_data(encrypted_data, output_path)
        logger.debug(f"Decrypted data stored at: {output_path}")
        return {"success": True}
    except Exception as e:
        logger.error(f"Error in retrieve_data: {e}")
        raise HTTPException(status_code=500, detail=str(e))

async def delete_data(ipfs_hash: str):
    try:
        logger.debug(f"Unpinning from Pinata with IPFS hash: {ipfs_hash}")
        response = unpin_from_pinata(ipfs_hash)
        logger.debug(f"Unpin response: {response}")
        return {"success": True, "response": response}
    except requests.exceptions.HTTPError as e:
        logger.error(f"Error in delete_data: {e}")
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in delete_data: {e}")
        raise HTTPException(status_code=500, detail=str(e))