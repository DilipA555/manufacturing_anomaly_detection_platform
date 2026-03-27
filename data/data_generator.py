import csv
import random
from datetime import datetime, timedelta
from config.config import Config


class DataGenerator:
    """Generates synthetic machine data"""

    def __init__(self):
        self.file_path = Config.DATA_FILE_PATH
        self.num_records = 10000

    def generate_data(self):
        """Generate CSV data"""
        try:
            with open(self.file_path, mode='w', newline='') as file:
                writer = csv.writer(file)

                # header
                writer.writerow([
                    "machine_id", "sector", "temperature",
                    "vibration", "pressure", "energy",
                    "production", "timestamp"
                ])

                sectors = list(Config.DEFAULT_THRESHOLDS.keys())

                for i in range(self.num_records):
                    sector = random.choice(sectors)
                    thresholds = Config.DEFAULT_THRESHOLDS[sector]

                    # decide type of data
                    data_type = random.random()

                    # normal data
                    if data_type < 0.75:
                        temperature = random.uniform(thresholds["temperature"] - 10, thresholds["temperature"])
                        vibration = random.uniform(thresholds["vibration"] - 0.5, thresholds["vibration"])
                        pressure = random.uniform(thresholds["pressure"] - 5, thresholds["pressure"])
                        energy = random.uniform(thresholds["energy"] - 100, thresholds["energy"])
                        production = random.uniform(thresholds["production"] - 20, thresholds["production"])

                    # anomaly data
                    elif data_type < 0.95:
                        temperature = random.uniform(thresholds["temperature"], thresholds["temperature"] + 30)
                        vibration = random.uniform(thresholds["vibration"], thresholds["vibration"] + 2)
                        pressure = random.uniform(thresholds["pressure"], thresholds["pressure"] + 20)
                        energy = random.uniform(thresholds["energy"], thresholds["energy"] + 200)
                        production = random.uniform(0, thresholds["production"])

                    # missing data
                    else:
                        # generate normal values first
                        temperature = random.uniform(20, thresholds["temperature"])
                        vibration = random.uniform(0.5, thresholds["vibration"])
                        pressure = random.uniform(10, thresholds["pressure"])
                        energy = random.uniform(100, thresholds["energy"])
                        production = random.uniform(10, thresholds["production"])

                        # randomly make some fields missing
                        if random.random() < 0.3:
                            temperature = None
                        if random.random() < 0.3:
                            vibration = None
                        if random.random() < 0.3:
                            pressure = None
                        if random.random() < 0.3:
                            energy = None
                        if random.random() < 0.3:
                            production = None

                    timestamp = datetime.now() - timedelta(minutes=i)

                    writer.writerow([
                        f"M_{i}",
                        sector,
                        temperature,
                        vibration,
                        pressure,
                        energy,
                        production,
                        timestamp
                    ])

            print("Data generation completed")

        except Exception as e:
            print(f"Error generating data: {e}")