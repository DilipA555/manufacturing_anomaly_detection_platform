from database.database_manager import DatabaseManager
from data.data_generator import DataGenerator
from data.data_ingestion import DataIngestion
from data.data_processor import DataProcessor
from detection.anomaly_detector import AnomalyDetector
from alerts.alert_manager import AlertManager


# setup db
db = DatabaseManager()
db.connect()
db.create_tables()
db.insert_thresholds()

# generate data
generator = DataGenerator()
generator.generate_data()

# load data
ingestion = DataIngestion()
data = ingestion.read_data()

# process data
processor = DataProcessor()
processed_data = processor.process_data(data)

# detect anomalies
detector = AnomalyDetector()
anomalies = detector.detect(processed_data)

# generate alerts
alert_manager = AlertManager()
alerts = alert_manager.generate_alerts(anomalies)

# write alerts to log file
with open("alerts.log", "w") as file:
    for alert in alerts:
        file.write(alert["message"] + "\n")

# store alerts in db
db.insert_anomalies(alerts)

# display summary
print("\n=== SYSTEM SUMMARY ===")
print(f"Total records processed: {len(processed_data)}")
print(f"Total anomalies detected: {len(anomalies)}")
print(f"Total alerts generated: {len(alerts)}")

# fetch recent alerts from DB
recent_alerts = db.fetch_anomalies()
print("\n=== RECENT ALERTS ===")
for alert in recent_alerts:
    print(
        f"Machine: {alert['machine_id']} | "
        f"Sector: {alert['sector']} | "
        f"Type: {alert['anomaly_type']} | "
        f"Value: {round(alert['value'], 2)} | "
        f"Time: {alert['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}"
    )

# sector analytics
analytics_data = db.get_anomaly_analytics()

sector_totals = {}
sector_parameter_breakdown = {}

for sector, parameter, count in analytics_data:
    sector_totals[sector] = sector_totals.get(sector, 0) + count

    if sector not in sector_parameter_breakdown:
        sector_parameter_breakdown[sector] = {}

    sector_parameter_breakdown[sector][parameter] = count

print("\n=== SECTOR SUMMARY ===")
for sector, total in sector_totals.items():
    print(f"{sector}: {total}")

print("\n=== PARAMETER BREAKDOWN ===")
for sector, parameters in sector_parameter_breakdown.items():
    print(f"\n{sector}:")
    for parameter, count in parameters.items():
        print(f"   {parameter}: {count}")

# close db
db.close()