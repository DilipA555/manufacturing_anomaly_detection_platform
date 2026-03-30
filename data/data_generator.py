from typing import Dict
import csv
import random
from datetime import datetime, timedelta
from config.config import Config


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
                    "machine_id", "sector", "temperature",
                    "vibration", "pressure", "energy",
                    "production", "timestamp"
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

                    # normal data
                    if data_type < 0.75:
                        values = self.generate_normal_values(thresholds)
                        temperature = values["temperature"]
                        vibration = values["vibration"]
                        pressure = values["pressure"]
                        energy = values["energy"]
                        production = values["production"]

                    # anomaly data
                    elif data_type < 0.95:
                        # start with normal values
                        values = self.generate_normal_values(thresholds)
                        temperature = values["temperature"]
                        vibration = values["vibration"]
                        pressure = values["pressure"]
                        energy = values["energy"]
                        production = values["production"]

                        # choose 1 or 2 parameters to be abnormal
                        anomaly_params = random.sample(
                            ["temperature", "vibration", "pressure", "energy", "production"],
                            k=random.randint(1, 2)
                        )

                        if "temperature" in anomaly_params:
                            temperature = random.uniform(thresholds["temperature"] * 1.05, thresholds["temperature"] * 1.3)

                        if "vibration" in anomaly_params:
                            vibration = random.uniform(thresholds["vibration"] * 1.2, thresholds["vibration"] * 2)

                        if "pressure" in anomaly_params:
                            pressure = random.uniform(thresholds["pressure"] * 1.1, thresholds["pressure"] * 1.5)

                        if "energy" in anomaly_params:
                            energy = random.uniform(thresholds["energy"] * 1.2, thresholds["energy"] * 1.5)

                        if "production" in anomaly_params:
                            production = random.uniform(thresholds["production"] * 0.3, thresholds["production"] * 0.7)

                    # missing data
                    else:
                        # generate normal values first
                        values = self.generate_normal_values(thresholds)
                        temperature = values["temperature"]
                        vibration = values["vibration"]
                        pressure = values["pressure"]
                        energy = values["energy"]
                        production = values["production"]

                        # randomly make some fields missing
                        if random.random() < 0.2:
                            temperature = None
                        if random.random() < 0.2:
                            vibration = None
                        if random.random() < 0.2:
                            pressure = None
                        if random.random() < 0.2:
                            energy = None
                        if random.random() < 0.2:
                            production = None
                        
                        # avoid all values becoming None
                        if all(v is None for v in [temperature, vibration, pressure, energy, production]):
                            field = random.choice(["temperature", "vibration", "pressure", "energy", "production"])

                            if field == "temperature":
                                temperature = random.uniform(thresholds["temperature"] - 10, thresholds["temperature"])
                            elif field == "vibration":
                                vibration = random.uniform(thresholds["vibration"] - 0.5, thresholds["vibration"])
                            elif field == "pressure":
                                pressure = random.uniform(thresholds["pressure"] - 5, thresholds["pressure"])
                            elif field == "energy":
                                energy = random.uniform(thresholds["energy"] - 100, thresholds["energy"])
                            elif field == "production":
                                production = random.uniform(thresholds["production"] - 20, thresholds["production"])

                    timestamp = datetime.now() - timedelta(minutes=5*i)

                    writer.writerow([
                        machine_id,
                        sector,
                        temperature,
                        vibration,
                        pressure,
                        energy,
                        production,
                        timestamp
                    ])

        except Exception as e:
            print(f"Error generating data: {e}")