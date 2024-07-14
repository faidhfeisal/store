import pytest
from unittest.mock import patch
from storage.pinata import upload_to_pinata, download_from_pinata, unpin_from_pinata

@patch('requests.post')
def test_upload_to_pinata(mock_post):
    mock_post.return_value.json.return_value = {'IpfsHash': 'mock_ipfs_hash'}
    result = upload_to_pinata(b'mock_data')
    mock_post.assert_called_once()
    assert result == 'mock_ipfs_hash'

@patch('requests.get')
def test_download_from_pinata(mock_get):
    mock_get.return_value.content = b'mock_data'
    result = download_from_pinata('mock_ipfs_hash')
    mock_get.assert_called_once()
    assert result == b'mock_data'

@patch('requests.delete')
def test_unpin_from_pinata(mock_delete):
    mock_delete.return_value.json.return_value = 'mock_response'
    result = unpin_from_pinata('mock_ipfs_hash')
    mock_delete.assert_called_once()
    assert result == 'mock_response'
