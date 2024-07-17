import requests
import json
from dotenv import load_dotenv
import os
from config import PINATA_API_URL, PINATA_API_KEY, PINATA_SECRET_API_KEY

# Load environment variables from .env file
load_dotenv()
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def upload_to_pinata(file_content, file_name):
    url = f'{PINATA_API_URL}/pinning/pinFileToIPFS'
    headers = {
            'pinata_api_key': PINATA_API_KEY,
            'pinata_secret_api_key': PINATA_SECRET_API_KEY
        }
    files = {
        'file': (file_name, file_content)
    }

    try:
        response = requests.post(url, headers=headers, files=files)
        logger.info(response)
        response.raise_for_status()
        return response.json()['IpfsHash']
    except requests.exceptions.RequestException as e:
        logger.error(f"Error uploading to Pinata: {e}")
        raise

def download_from_pinata(ipfs_hash):
    url = f'https://gateway.pinata.cloud/ipfs/{ipfs_hash}'
    try:
        response = requests.get(url)
        logger.info(f"Pinata response status: {response.status_code}")
        logger.info(f"Pinata response: {response}")
        response.raise_for_status()
        content = response.content
        if content is None or len(content) == 0:
            logger.error("Received empty content from Pinata")
            raise ValueError("Received empty content from Pinata")
        logger.info(f"Downloaded content length: {len(content)}")
        
        # Decode the content and parse it as JSON
        content_json = json.loads(content.decode('utf-8'))
        logger.info(f"Parsed JSON content: {content_json}")
        
        return content_json
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON from Pinata: {str(e)}")
        raise
    except requests.exceptions.RequestException as e:
        logger.error(f"Error downloading from Pinata: {str(e)}")
        raise

def unpin_from_pinata(ipfs_hash):
    headers = {
        "pinata_api_key": PINATA_API_KEY,
        "pinata_secret_api_key": PINATA_SECRET_API_KEY
    }
    url = f'{PINATA_API_URL}/pinning/unpin/{ipfs_hash}'
    logger.info(f"Unpin URL: {url}")
    
    try:
        response = requests.delete(url, headers=headers)
        response.raise_for_status()  # This will raise an exception for HTTP errors
        logger.info(f"Successfully unpinned {ipfs_hash}")
        return {"success": True, "message": f"Successfully unpinned {ipfs_hash}"}
    except requests.exceptions.RequestException as e:
        logger.error(f"Error unpinning from Pinata: {str(e)}")
        return {"success": False, "error": str(e)}