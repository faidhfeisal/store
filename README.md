# Store Service

## Overview
The Store Service is responsible for managing the storage and retrieval of static data assets in the OwnIt Marketplace. It uses IPFS via Pinata for decentralized storage and implements encryption for data security.

## Features
- Store encrypted data on IPFS
- Retrieve and decrypt data from IPFS
- Delete (unpin) data from IPFS

## Setup

### 1. Pinata Account Setup
Before running the Store Service, you need to set up a Pinata account:

1. Go to [Pinata](https://www.pinata.cloud/) and sign up for an account.
2. Once logged in, navigate to the API Keys section.
3. Create a new API key with the necessary permissions (pinning, unpinning).
4. Note down your API Key and API Secret.

### 2. Environment Variables
Create a `.env` file in the root directory and add the following:

```
PINATA_API_URL=https://api.pinata.cloud
PINATA_API_KEY=<your_pinata_api_key>
PINATA_SECRET_API_KEY=<your_pinata_secret_api_key>
```

Replace `<your_pinata_api_key>` and `<your_pinata_secret_api_key>` with the API Key and API Secret you obtained from Pinata.

### 3. Install Dependencies
Install the required Python packages:

```
pip install -r requirements.txt
```

### 4. Run the Service
Start the Store Service:

```
python main.py
```

## API Endpoints

- POST `/store`: Store a file (encrypts and uploads to IPFS)
- POST `/retrieve`: Retrieve a file by IPFS hash (downloads and decrypts)
- POST `/delete`: Delete (unpin) a file from IPFS

## Key Components

### Pinata Integration
The service uses Pinata's API to interact with IPFS for storing and retrieving data.

### Encryption
Data is encrypted using AES-256-GCM before being stored on IPFS, ensuring the confidentiality of stored assets.

### Data Management
The `data_manager.py` module orchestrates the process of storing, retrieving, and deleting data, integrating encryption and Pinata interactions.


## Security Considerations
- Protect the Pinata API keys in the environment variables
- Implement access control to ensure only authorized services can store and retrieve data
- Regularly rotate encryption keys and update the encryption implementation as needed
- Monitor and limit API usage to prevent abuse
- Implement proper error handling and logging for all operations
