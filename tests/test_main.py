import pytest
from fastapi.testclient import TestClient
from main import app
from unittest.mock import patch, mock_open

client = TestClient(app)

@patch('storage.main.store_data')
def test_store_data_endpoint(mock_store_data):
    mock_store_data.return_value = {"success": True, "ipfs_hash": "mock_ipfs_hash"}
    response = client.post("/store", json={"file_path": "test_file.txt"})
    assert response.status_code == 200
    assert response.json() == {"success": True, "ipfs_hash": "mock_ipfs_hash"}

@patch('storage.main.retrieve_data')
def test_retrieve_data_endpoint(mock_retrieve_data):
    mock_retrieve_data.return_value = {"success": True}
    response = client.post("/retrieve", json={"ipfs_hash": "mock_ipfs_hash", "output_path": "output_file.txt"})
    assert response.status_code == 200
    assert response.json() == {"success": True}

@patch('storage.main.delete_data')
def test_delete_data_endpoint(mock_delete_data):
    mock_delete_data.return_value = {"success": True, "response": "mock_response"}
    response = client.post("/delete", json={"ipfs_hash": "mock_ipfs_hash"})
    assert response.status_code == 200
    assert response.json() == {"success": True, "response": "mock_response"}
