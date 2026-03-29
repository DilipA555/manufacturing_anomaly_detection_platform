from typing import List, Dict, Any
from config.config import Config


class AnomalyDetector:
    """Detects anomalies based on threshold values with tolerance"""


    def detect(self, processed_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Check each record for anomalies"""

        anomalies = []

        for record in processed_data:
            sector = record["sector"]
            thresholds = Config.DEFAULT_THRESHOLDS.get(sector, {})

            anomaly_flags = {}

            # extract values
            temperature = record["temperature"]
            vibration = record["vibration"]
            pressure = record["pressure"]
            energy = record["energy"]
            production = record["production"]

            # extract thresholds
            temperature_threshold = thresholds.get("temperature")
            vibration_threshold = thresholds.get("vibration")
            pressure_threshold = thresholds.get("pressure")
            energy_threshold = thresholds.get("energy")
            production_threshold = thresholds.get("production")

            # apply tolerance-based checks
            if temperature is not None and temperature > temperature_threshold * 1.1:
                anomaly_flags["temperature"] = temperature

            if vibration is not None and vibration > vibration_threshold * 1.2:
                anomaly_flags["vibration"] = vibration

            if pressure is not None and pressure > pressure_threshold * 1.1:
                anomaly_flags["pressure"] = pressure

            if energy is not None and energy > energy_threshold * 1.2:
                anomaly_flags["energy"] = energy

            if production is not None and production < production_threshold * 0.7:
                anomaly_flags["production"] = production

            # store anomaly if any condition triggered
            if anomaly_flags:
                anomalies.append({
                    "machine_id": record["machine_id"],
                    "sector": sector,
                    "anomalies": anomaly_flags,
                    "timestamp": record["timestamp"]
                })

        return anomalies