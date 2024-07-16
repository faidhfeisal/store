# config.py
import os
from dotenv import load_dotenv

load_dotenv()

# Pinata configuration
PINATA_API_URL = os.getenv('PINATA_API_URL')
PINATA_API_KEY = os.getenv('PINATA_API_KEY')
PINATA_SECRET_API_KEY = os.getenv('PINATA_SECRET_API_KEY')

