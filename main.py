from database.database_manager import DatabaseManager
from data.data_generator import DataGenerator
from data.data_ingestion import DataIngestion
from data.data_processor import DataProcessor
from detection.anomaly_detector import AnomalyDetector
from alerts.alert_manager import AlertManager


# test database connection and table creation
db = DatabaseManager()
db.connect()
db.create_tables()
db.insert_thresholds()

# test data generation
generator = DataGenerator()
generator.generate_data()

# test data ingestion
ingestion = DataIngestion()
data = ingestion.read_data()
print(f"Total records loaded: {len(data)}")

# test data processor
processor = DataProcessor()
processed_data = processor.process_data(data)
print(f"Processed records: {len(processed_data)}")

# test anomaly detector
detector = AnomalyDetector()
anomalies = detector.detect(processed_data)
print(f"Total anomalies detected: {len(anomalies)}")

# test alert manager
alert_manager = AlertManager()
alerts = alert_manager.generate_alerts(anomalies)
print(f"Total alerts generated: {len(alerts)}")

# write alerts to log file
with open("alerts.log", "w") as file:
    for alert in alerts:
        file.write(alert["message"] + "\n")
print("Alerts written to alerts.log")

#  store generated alerts into database
db.insert_anomalies(alerts)

# fetch recent alerts from DB
recent_alerts = db.fetch_anomalies()
print("\nRecent Alerts from Database:")
for alert in recent_alerts:
    print(
        f"Machine: {alert['machine_id']} | "
        f"Sector: {alert['sector']} | "
        f"Type: {alert['anomaly_type']} | "
        f"Value: {alert['value']} | "
        f"Time: {alert['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}"
    )

db.close()