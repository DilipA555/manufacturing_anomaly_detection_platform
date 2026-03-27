from utils.helpers import format_alert_message


class AlertManager:
    """Handles alert generation from detected anomalies"""

    def generate_alerts(self, anomalies):
        """Convert anomalies into structured alert data"""

        alerts = []

        for anomaly in anomalies:
            machine_id = anomaly["machine_id"]
            sector = anomaly["sector"]
            timestamp = anomaly["timestamp"]

            anomaly_details = anomaly["anomalies"]

            for parameter, value in anomaly_details.items():

                message = format_alert_message(
                    machine_id,
                    sector,
                    parameter,
                    value
                )

                alerts.append({
                    "machine_id": machine_id,
                    "sector": sector,
                    "parameter": parameter,
                    "value": value,
                    "message": message,
                    "timestamp": timestamp
                })

        return alerts