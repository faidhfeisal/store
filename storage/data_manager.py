from fastapi import HTTPException
from .pinata import upload_to_pinata, download_from_pinata, unpin_from_pinata
from .encryption import encrypt_data, decrypt_data

def store_data(file_path: str):
    try:
        encrypted_data = encrypt_data(file_path)
        ipfs_hash = upload_to_pinata(encrypted_data)
        return {"success": True, "ipfs_hash": ipfs_hash}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def retrieve_data(ipfs_hash: str, output_path: str):
    try:
        encrypted_data = download_from_pinata(ipfs_hash)
        decrypt_data(encrypted_data, output_path)
        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def delete_data(ipfs_hash: str):
    try:
        response = unpin_from_pinata(ipfs_hash)
        return {"success": True, "response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))