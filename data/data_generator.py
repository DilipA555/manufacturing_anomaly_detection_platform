from typing import Dict
import csv
import random
from datetime import datetime, timedelta
from config.config import Config


PARAMS = ["temperature", "vibration", "pressure", "energy", "production"]
# rule-based anomaly logic
ANOMALY_RULES = {
    "temperature": lambda t: random.uniform(t * 1.05, t * 1.3),
    "vibration": lambda t: random.uniform(t * 1.2, t * 2),
    "pressure": lambda t: random.uniform(t * 1.1, t * 1.5),
    "energy": lambda t: random.uniform(t * 1.2, t * 1.5),
    "production": lambda t: random.uniform(t * 0.3, t * 0.7)
}

class DataGenerator:
    """Generates synthetic machine data"""


    def generate_normal_values(self, thresholds: Dict[str, float]) -> Dict[str, float]:
        """Generate normal sensor values based on sector thresholds."""

        return {
            "temperature": random.uniform(thresholds["temperature"] - 10, thresholds["temperature"]),
            "vibration": random.uniform(thresholds["vibration"] - 0.5, thresholds["vibration"]),
            "pressure": random.uniform(thresholds["pressure"] - 5, thresholds["pressure"]),
            "energy": random.uniform(thresholds["energy"] - 100, thresholds["energy"]),
            "production": random.uniform(thresholds["production"] - 20, thresholds["production"])
        }

    def __init__(self):

        self.file_path = Config.DATA_FILE_PATH
        self.num_records = 10000

    def generate_data(self) -> None:
        """Generate CSV data"""
        
        try:
            with open(self.file_path, mode='w', newline='') as file:
                writer = csv.writer(file)

                # header
                writer.writerow([
                    "machine_id", "sector", *PARAMS, "timestamp"
                ])

                sectors = list(Config.DEFAULT_THRESHOLDS.keys())

                # fixed machines per sector
                machines_per_sector = {
                    "Automotive": [f"A_{i}" for i in range(1, 21)],
                    "Electronics": [f"E_{i}" for i in range(1, 21)],
                    "Steel": [f"S_{i}" for i in range(1, 21)]
                }

                for i in range(self.num_records):
                    sector = random.choice(sectors)
                    thresholds = Config.DEFAULT_THRESHOLDS[sector]

                    machine_id = random.choice(machines_per_sector[sector])

                    # decide type of data
                    data_type = random.random()

                    # generate normal data
                    data = self.generate_normal_values(thresholds)

                    # anomaly case
                    if 0.75 <= data_type < 0.95:
                        anomaly_params = random.sample(PARAMS, k=random.randint(1, 2))

                        for param in anomaly_params:
                            data[param] = ANOMALY_RULES[param](thresholds[param])

                    # missing case
                    elif data_type >= 0.95:
                        # choose how many params to make missing
                        num_missing = random.randint(1, 2)
                        missing_params = random.sample(PARAMS, k=num_missing)

                        for param in missing_params:
                            data[param] = None

                    # timestamp
                    timestamp = datetime.now() - timedelta(minutes=5*i)

                    # write data
                    writer.writerow([
                        machine_id,
                        sector,
                        *[data[param] for param in PARAMS],
                        timestamp
                    ])

        except Exception as e:
            print(f"Error generating data: {e}")