from typing import List, Dict, Any
from datetime import datetime
from collections import defaultdict


PARAMS = ["temperature", "vibration", "pressure", "energy", "production"]

class DataProcessor:
    """Handles data cleaning and missing value filling"""


    def process_data(self, data: List[Dict[str, str]]) -> List[Dict[str, Any]]:
        """Process raw data and fill missing values using sector averages"""

        # store sums and counts per sector
        sector_stats = defaultdict(lambda: {param: 0 for param in PARAMS} | {"count": 0})

        # calculate totals
        for row in data:
            try:
                sector = row["sector"]

                values = {
                    param: float(row[param]) if row[param] not in ("", None) else None
                    for param in PARAMS
                }

                if all(v is None for v in values.values()):
                    continue

                sector_stats[sector]["count"] += 1

                for param, value in values.items():
                    if value is not None:
                        sector_stats[sector][param] += value

            except Exception:
                continue

        # calculate averages per sector
        sector_averages = {}

        for sector, values in sector_stats.items():
            count = values["count"] or 1

            sector_averages[sector] = {
                param: values[param] / count for param in PARAMS
            }

        processed_data = []

        # fill missing values using averages
        for row in data:
            try:
                sector = row["sector"]
                averages = sector_averages.get(sector, {})

                values = {
                    param: float(row[param]) if row[param] not in ("", None)
                    else averages.get(param, 0)
                    for param in PARAMS
                }

                timestamp = datetime.strptime(row["timestamp"], "%Y-%m-%d %H:%M:%S.%f")

                processed_data.append({
                    "machine_id": row["machine_id"],
                    "sector": sector,
                    **values,
                    "timestamp": timestamp
                })

            except Exception:
                continue

        return processed_data