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

    # default thresholds (units mentioned)
    DEFAULT_THRESHOLDS = {
        "Automotive": {
            "temperature": 90,   # °C
            "vibration": 1.2,    # mm/s
            "pressure": 40,      # bar
            "energy": 600,       # kWh
            "production": 80     # units/hour
        },
        "Electronics": {
            "temperature": 80,   # °C
            "vibration": 1.0,    # mm/s
            "pressure": 35,      # bar
            "energy": 500,       # kWh
            "production": 150    # units/hour
        },
        "Steel": {
            "temperature": 120,  # °C
            "vibration": 2.0,    # mm/s
            "pressure": 50,      # bar
            "energy": 900,       # kWh
            "production": 40     # units/hour
        }
    }