from typing import List, Dict, Any
from config.config import Config


PARAMS = ["temperature", "vibration", "pressure", "energy", "production"]

ANOMALY_RULES = {
    "temperature": lambda val, th: val > th * 1.1,
    "vibration": lambda val, th: val > th * 1.2,
    "pressure": lambda val, th: val > th * 1.1,
    "energy": lambda val, th: val > th * 1.2,
    "production": lambda val, th: val < th * 0.7
}

class AnomalyDetector:
    """Detects anomalies based on threshold values with tolerance"""


    def detect(self, processed_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Check each record for anomalies"""

        anomalies = []

        for record in processed_data:
            sector = record["sector"]
            thresholds = Config.DEFAULT_THRESHOLDS.get(sector, {})

            anomaly_flags = {}

            for param in PARAMS:
                value = record[param]
                threshold = thresholds.get(param)

                if value is not None and threshold is not None:
                    if ANOMALY_RULES[param](value, threshold):
                        anomaly_flags[param] = value

            # store anomaly if any condition triggered
            if anomaly_flags:
                anomalies.append({
                    "machine_id": record["machine_id"],
                    "sector": sector,
                    "anomalies": anomaly_flags,
                    "timestamp": record["timestamp"]
                })

        return anomalies