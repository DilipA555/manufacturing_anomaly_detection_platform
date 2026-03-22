import os
from dotenv import load_dotenv

# load values from .env file
load_dotenv()


class Config:
    """Stores configuration values"""

    # database config
    DB_HOST = os.getenv("DB_HOST")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_NAME = os.getenv("DB_NAME")

    # file path
    DATA_FILE_PATH = "data/manufacturing_data.csv"

    # logging file
    LOG_FILE = "logs/system.log"