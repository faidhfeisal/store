import requests
import os

# Configuration for Pinata
PINATA_API_URL = os.getenv('PINATA_API_URL')
PINATA_API_KEY = os.getenv('PINATA_API_KEY')

headers = {
    "Authorization": "Bearer {}".format(PINATA_API_KEY),
    "Content-Type": "multipart/form-data"
}

def upload_to_pinata(data):
    url = f'{PINATA_API_URL}/pinning/pinFileToIPFS'
    files = {'file': data}
    response = requests.post(url, files=files, headers=headers)
    response.raise_for_status()
    return response.json()['IpfsHash']

def download_from_pinata(ipfs_hash):
    url = f'https://gateway.pinata.cloud/ipfs/{ipfs_hash}'
    response = requests.get(url)
    response.raise_for_status()
    return response.content

def unpin_from_pinata(ipfs_hash):
    url = f'{PINATA_API_URL}/pinning/unpin/{ipfs_hash}'
    response = requests.delete(url, headers=headers)
    response.raise_for_status()
    return response.json()
