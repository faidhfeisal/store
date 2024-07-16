import pytest
import os
from unittest.mock import patch, mock_open, MagicMock
from storage.data_manager import store_data, retrieve_data, delete_data

@pytest.fixture
def mock_pinata():
    with patch('storage.data_manager.upload_to_pinata') as mock_upload, \
         patch('storage.data_manager.download_from_pinata') as mock_download, \
         patch('storage.data_manager.unpin_from_pinata') as mock_unpin:
        yield mock_upload, mock_download, mock_unpin

@pytest.fixture
def mock_encryption():
    with patch('storage.data_manager.encrypt_data') as mock_encrypt, \
         patch('storage.data_manager.decrypt_data') as mock_decrypt:
        yield mock_encrypt, mock_decrypt

def test_store_data(mock_pinata, mock_encryption):
    mock_upload, _, _ = mock_pinata
    mock_encrypt, _ = mock_encryption
    mock_encrypt.return_value = "encrypted_data"
    mock_upload.return_value = "mock_ipfs_hash"
    
    result = store_data("test_file.txt")
    
    mock_encrypt.assert_called_once_with("test_file.txt")
    mock_upload.assert_called_once_with("encrypted_data")
    assert result == {"success": True, "ipfs_hash": "mock_ipfs_hash"}

def test_retrieve_data(mock_pinata, mock_encryption):
    _, mock_download, _ = mock_pinata
    _, mock_decrypt = mock_encryption
    mock_download.return_value = "encrypted_data"
    
    result = retrieve_data("mock_ipfs_hash", "output_file.txt")
    
    mock_download.assert_called_once_with("mock_ipfs_hash")
    mock_decrypt.assert_called_once_with("encrypted_data", "output_file.txt")
    assert result == {"success": True}

@patch.dict(os.environ, {"PINATA_API_URL": "https://mock.pinata.cloud", "PINATA_API_KEY": "test_key"})
@patch('requests.delete')
def test_delete_data(mock_delete):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"response": "mock_response"}
    mock_delete.return_value = mock_response
    
    print("Mock PINATA_API_URL:", os.getenv("PINATA_API_URL"))  # Debug print to verify environment variable
    print("Mock PINATA_API_KEY:", os.getenv("PINATA_API_KEY"))  # Debug print to verify environment variable

    result = delete_data("mock_ipfs_hash")
    
    mock_delete.assert_called_once_with(
        "https://mock.pinata.cloud/pinning/unpin/mock_ipfs_hash",
        headers={
            "Authorization": "Bearer test_key",
            "Content-Type": "application/json"
        }
    )
    print("Delete data result:", result)  # Debug print to verify the result
    assert result == {"success": True, "response": {"response": "mock_response"}}
