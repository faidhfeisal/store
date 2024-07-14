from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA256
import hashlib
import os
import json
import random

# Constants
SALT_SIZE = 16
KEY_SIZE = 32
NONCE_SIZE = 16
TAG_SIZE = 16

class ZKProof:
    def __init__(self):
        self.N = 20
        self.salt = os.urandom(16)

    def _hash(self, x):
        return hashlib.sha256(x.encode('utf-8') + self.salt).hexdigest()

    def generate_proof(self, secret):
        self.secret = secret
        self.v = self._hash(secret)
        r = str(random.randint(1, self.N))
        self.x = self._hash(r)
        return self.x

    def get_secret(self):
        return self.secret

    def verify(self, response):
        return self.v == self._hash(response)

zkp = ZKProof()

def encrypt_data(file_path):
    with open(file_path, 'rb') as file:
        data = file.read()

    # Generate a random salt
    salt = get_random_bytes(SALT_SIZE)

    # Derive a key using PBKDF2
    password = b"secure_password"  # Replace with a secure password or key management system
    key = PBKDF2(password, salt, dkLen=KEY_SIZE, count=1000000, hmac_hash_module=SHA256)

    # Create a cipher object using the key
    cipher = AES.new(key, AES.MODE_GCM)

    # Encrypt the data
    ciphertext, tag = cipher.encrypt_and_digest(data)

    # Generate ZKP proof
    proof = zkp.generate_proof(data.decode())

    # Combine salt, nonce, tag, proof, and ciphertext
    encrypted_data = {
        'salt': salt.hex(),
        'nonce': cipher.nonce.hex(),
        'tag': tag.hex(),
        'proof': proof,
        'ciphertext': ciphertext.hex()
    }

    return json.dumps(encrypted_data)

def decrypt_data(encrypted_data, output_path):
    # Parse the encrypted data
    encrypted_data = json.loads(encrypted_data)
    salt = bytes.fromhex(encrypted_data['salt'])
    nonce = bytes.fromhex(encrypted_data['nonce'])
    tag = bytes.fromhex(encrypted_data['tag'])
    proof = encrypted_data['proof']
    ciphertext = bytes.fromhex(encrypted_data['ciphertext'])

    # Derive the key using PBKDF2
    password = b"secure_password"  # Replace with a secure password or key management system
    key = PBKDF2(password, salt, dkLen=KEY_SIZE, count=1000000, hmac_hash_module=SHA256)

    # Create a cipher object using the key
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)

    # Decrypt the data
    data = cipher.decrypt_and_verify(ciphertext, tag)

    # Verify ZKP proof
    if not zkp.verify(data.decode()):
        raise ValueError("ZKP proof verification failed")

    # Write the decrypted data to the output file
    with open(output_path, 'wb') as file:
        file.write(data)
