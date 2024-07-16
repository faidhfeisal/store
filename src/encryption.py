from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA256
import os
import json

# Constants
SALT_SIZE = 16
KEY_SIZE = 32
NONCE_SIZE = 16
TAG_SIZE = 16

def encrypt_data(data: bytes):
    # Generate a random salt
    salt = get_random_bytes(SALT_SIZE)

    # Derive a key using PBKDF2
    password = b"secure_password"  # Replace with a secure password or key management system
    key = PBKDF2(password, salt, dkLen=KEY_SIZE, count=1000000, hmac_hash_module=SHA256)

    # Create a cipher object using the key
    cipher = AES.new(key, AES.MODE_GCM)

    # Encrypt the data
    ciphertext, tag = cipher.encrypt_and_digest(data)

    # Combine salt, nonce, tag, and ciphertext
    encrypted_data = {
        'salt': salt.hex(),
        'nonce': cipher.nonce.hex(),
        'tag': tag.hex(),
        'ciphertext': ciphertext.hex()
    }

    return json.dumps(encrypted_data).encode()

def decrypt_data(encrypted_data, output_path):
    # Parse the encrypted data
    encrypted_data = json.loads(encrypted_data)
    salt = bytes.fromhex(encrypted_data['salt'])
    nonce = bytes.fromhex(encrypted_data['nonce'])
    tag = bytes.fromhex(encrypted_data['tag'])
    ciphertext = bytes.fromhex(encrypted_data['ciphertext'])

    # Derive the key using PBKDF2
    password = b"secure_password"  # Replace with a secure password or key management system
    key = PBKDF2(password, salt, dkLen=KEY_SIZE, count=1000000, hmac_hash_module=SHA256)

    # Create a cipher object using the key
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)

    # Decrypt the data
    data = cipher.decrypt_and_verify(ciphertext, tag)

    # Write the decrypted data to the output file
    with open(output_path, 'wb') as file:
        file.write(data)

async def encrypt_data_streaming(file_object):
    salt = get_random_bytes(SALT_SIZE)
    password = b"secure_password"  # Replace with a secure password or key management system
    key = PBKDF2(password, salt, dkLen=KEY_SIZE, count=1000000, hmac_hash_module=SHA256)

    cipher = AES.new(key, AES.MODE_GCM)
    
    yield salt
    yield cipher.nonce

    while True:
        chunk = await file_object.read(CHUNK_SIZE)
        if not chunk:
            break
        encrypted_chunk = cipher.encrypt(chunk)
        yield encrypted_chunk

    tag = cipher.digest()
    yield tag

async def decrypt_data_streaming(encrypted_stream, output_file):
    salt = await encrypted_stream.read(SALT_SIZE)
    nonce = await encrypted_stream.read(NONCE_SIZE)

    password = b"secure_password"  # Replace with a secure password or key management system
    key = PBKDF2(password, salt, dkLen=KEY_SIZE, count=1000000, hmac_hash_module=SHA256)

    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)

    with open(output_file, 'wb') as f:
        while True:
            chunk = await encrypted_stream.read(CHUNK_SIZE)
            if len(chunk) == 0:
                break
            decrypted_chunk = cipher.decrypt(chunk)
            f.write(decrypted_chunk)

    tag = await encrypted_stream.read(TAG_SIZE)
    try:
        cipher.verify(tag)
    except ValueError:
        os.remove(output_file)  # Delete the output file if verification fails
        raise ValueError("MAC check failed")

# Helper function to securely generate a key
def generate_key():
    return get_random_bytes(KEY_SIZE)

# Helper function to securely store a key (this is a simple example, consider using a proper key management system in production)
def store_key(key, key_file):
    with open(key_file, 'wb') as f:
        f.write(key)

# Helper function to securely load a key (this is a simple example, consider using a proper key management system in production)
def load_key(key_file):
    with open(key_file, 'rb') as f:
        return f.read()