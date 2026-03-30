from typing import List, Dict, Any
from datetime import datetime
from collections import defaultdict


class DataProcessor:
    """Handles data cleaning and missing value filling"""


    def process_data(self, data: List[Dict[str, str]]) -> List[Dict[str, Any]]:
        """Process raw data and fill missing values using sector averages"""

        # store sums and counts per sector
        sector_stats = defaultdict(lambda: {
            "temperature": 0,
            "vibration": 0,
            "pressure": 0,
            "energy": 0,
            "production": 0,
            "count": 0
        })

        # calculate totals
        for row in data:
            try:
                sector = row["sector"]

                temperature = float(row["temperature"]) if row["temperature"] not in ("", None) else None
                vibration = float(row["vibration"]) if row["vibration"] not in ("", None) else None
                pressure = float(row["pressure"]) if row["pressure"] not in ("", None) else None
                energy = float(row["energy"]) if row["energy"] not in ("", None) else None
                production = float(row["production"]) if row["production"] not in ("", None) else None

                if all(value is None for value in [temperature, vibration, pressure, energy, production]):
                    continue

                sector_stats[sector]["count"] += 1

                if temperature is not None:
                    sector_stats[sector]["temperature"] += temperature
                if vibration is not None:
                    sector_stats[sector]["vibration"] += vibration
                if pressure is not None:
                    sector_stats[sector]["pressure"] += pressure
                if energy is not None:
                    sector_stats[sector]["energy"] += energy
                if production is not None:
                    sector_stats[sector]["production"] += production

            except Exception:
                continue

        # calculate averages per sector
        sector_averages = {}

        for sector, values in sector_stats.items():
            count = values["count"] or 1

            sector_averages[sector] = {
                "temperature": values["temperature"] / count,
                "vibration": values["vibration"] / count,
                "pressure": values["pressure"] / count,
                "energy": values["energy"] / count,
                "production": values["production"] / count
            }

        processed_data = []

        # fill missing values using averages
        for row in data:
            try:
                sector = row["sector"]
                averages = sector_averages.get(sector, {})

                temperature = float(row["temperature"]) if row["temperature"] not in ("", None) else averages.get("temperature", 0)
                vibration = float(row["vibration"]) if row["vibration"] not in ("", None) else averages.get("vibration", 0)
                pressure = float(row["pressure"]) if row["pressure"] not in ("", None) else averages.get("pressure", 0)
                energy = float(row["energy"]) if row["energy"] not in ("", None) else averages.get("energy", 0)
                production = float(row["production"]) if row["production"] not in ("", None) else averages.get("production", 0)

                timestamp = datetime.strptime(row["timestamp"], "%Y-%m-%d %H:%M:%S.%f")

                processed_data.append({
                    "machine_id": row["machine_id"],
                    "sector": sector,
                    "temperature": temperature,
                    "vibration": vibration,
                    "pressure": pressure,
                    "energy": energy,
                    "production": production,
                    "timestamp": timestamp
                })

            except Exception:
                continue

        return processed_data