import pytest
import logging
from fastapi.testclient import TestClient
from unittest.mock import patch, mock_open, MagicMock
from main import app
import os

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(level=logging.DEBUG)

client = TestClient(app)

@patch.dict(os.environ, {"PINATA_API_URL": "https://mock.pinata.cloud", "PINATA_API_KEY": "test_key"})
@patch('builtins.open', new_callable=mock_open, read_data=b"data")  # Use bytes instead of string
@patch('requests.post')
def test_store_data_endpoint(mock_post, mock_file):
    # Mock the response from requests.post
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"IpfsHash": "mock_ipfs_hash"}
    mock_post.return_value = mock_response
    
    response = client.post("/store", json={"file_path": "test_file.txt"})
    logging.debug(response.json())
    assert response.status_code == 200, f"Response content: {response.content}"
    assert response.json() == {"success": True, "ipfs_hash": "mock_ipfs_hash"}

@patch.dict(os.environ, {"PINATA_API_URL": "https://mock.pinata.cloud", "PINATA_API_KEY": "test_key"})
@patch('requests.get')
@patch('storage.data_manager.decrypt_data')
def test_retrieve_data_endpoint(mock_decrypt_data, mock_get):
    # Mock the response from requests.get
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = b"mock_encrypted_data"
    mock_get.return_value = mock_response
    
    mock_decrypt_data.return_value = None  # Ensure decrypt_data does not perform any real operation

    response = client.post("/retrieve", json={"ipfs_hash": "mock_ipfs_hash", "output_path": "output_file.txt"})
    logging.debug(response.json())
    assert response.status_code == 200, f"Response content: {response.content}"
    assert response.json() == {"success": True}

@patch.dict(os.environ, {"PINATA_API_URL": "https://mock.pinata.cloud", "PINATA_API_KEY": "test_key"})
@patch('requests.delete')
def test_delete_data_endpoint(mock_delete):
    # Mock the response from requests.delete
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"response": "mock_response"}
    mock_delete.return_value = mock_response
    
    response = client.post("/delete", json={"ipfs_hash": "mock_ipfs_hash"})
    logging.debug(response.json())
    assert response.status_code == 200, f"Response content: {response.content}"
    assert response.json() == {"success": True, "response": {"response": "mock_response"}}
