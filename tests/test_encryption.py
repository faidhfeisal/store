import pytest
import json
from unittest.mock import patch, mock_open
from storage.encryption import encrypt_data, decrypt_data

@patch("builtins.open", new_callable=mock_open, read_data=b"mock_data")
@patch("storage.encryption.zkp.generate_proof", return_value="mock_proof")
def test_encrypt_data(mock_generate_proof, mock_file):
    result = encrypt_data("test_file.txt")
    assert "proof" in result
    assert "ciphertext" in result

@patch("builtins.open", new_callable=mock_open)
@patch("storage.encryption.zkp.verify", return_value=True)
def test_decrypt_data(mock_verify, mock_file):
    # First, encrypt the data to get a consistent encrypted data structure
    with patch("builtins.open", new_callable=mock_open, read_data=b"mock_data"):
        encrypted_data_str = encrypt_data("test_file.txt")

    # Now, decrypt the data using the same structure
    decrypt_data(encrypted_data_str, "output_file.txt")
    mock_verify.assert_called_once_with("mock_data")

    # Ensure the decrypted data is written to the output file
    mock_file().write.assert_called_once_with(b"mock_data")
