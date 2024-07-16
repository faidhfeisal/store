import requests
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
    response = requests.get(url)
    response.raise_for_status()
    return response.content

def unpin_from_pinata(ipfs_hash):
    headers = {
        "Authorization": f"Bearer {PINATA_API_KEY}",
        "Content-Type": "application/json"
    }
    url = f'{PINATA_API_URL}/pinning/unpin/{ipfs_hash}'
    logger.debug(f"Unpin URL: {url}")  # Debug print to verify the URL
    response = requests.delete(url, headers=headers)
    response.raise_for_status()
    return response.json()