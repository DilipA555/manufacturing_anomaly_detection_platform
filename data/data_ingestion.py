from typing import List, Dict
import csv
from config.config import Config


class DataIngestion:
    """Reads data from CSV file"""


    def __init__(self):

        self.file_path = Config.DATA_FILE_PATH

    def read_data(self) -> List[Dict[str, str]]:
        """Read CSV and return data as list of dictionaries"""
        
        data = []

        try:
            with open(self.file_path, mode='r') as file:
                reader = csv.DictReader(file)

                for row in reader:
                    data.append(row)

            return data

        except Exception as e:
            print(f"Error reading data: {e}")
            return []