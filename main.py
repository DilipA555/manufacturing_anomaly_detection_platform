from typing import Dict, Any
from database.database_manager import DatabaseManager
from data.data_generator import DataGenerator
from data.data_ingestion import DataIngestion
from data.data_processor import DataProcessor
from detection.anomaly_detector import AnomalyDetector
from alerts.alert_manager import AlertManager
import logging
import cProfile
import tracemalloc


# configure logging for system monitoring
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def run_pipeline() -> Dict[str, Any]:
    
    tracemalloc.start()
    # setup db
    db = DatabaseManager()
    db.connect()
    db.create_tables()
    db.insert_thresholds()

    # generate data
    generator = DataGenerator()
    generator.generate_data()
    logging.info("Data generation completed")

    # load data
    ingestion = DataIngestion()
    data = ingestion.read_data()
    logging.info(f"Loaded {len(data)} records")

    # process data
    processor = DataProcessor()
    processed_data = processor.process_data(data)
    logging.info("Data processing completed")

    # detect anomalies
    detector = AnomalyDetector()
    anomalies = detector.detect(processed_data)
    logging.info(f"Detected {len(anomalies)} anomalies")

    # generate alerts
    alert_manager = AlertManager()
    alerts = alert_manager.generate_alerts(anomalies)
    logging.info(f"Generated {len(alerts)} alerts")

    # write alerts to log file
    with open("alerts.log", "w") as file:
        for alert in alerts:
            file.write(alert["message"] + "\n")

    # store alerts in db
    db.insert_anomalies(alerts)
    logging.info("Alerts stored in database")

    # fetch recent alerts from DB
    recent_alerts = db.fetch_anomalies()

    # sector analytics
    analytics_data = db.get_anomaly_analytics()

    sector_totals = {}
    sector_parameter_breakdown = {}

    for sector, parameter, count in analytics_data:
        sector_totals[sector] = sector_totals.get(sector, 0) + count

        if sector not in sector_parameter_breakdown:
            sector_parameter_breakdown[sector] = {}

        sector_parameter_breakdown[sector][parameter] = count

    # close db
    db.close()

    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return {
    "processed_data": processed_data,
    "anomalies": anomalies,
    "alerts": alerts,
    "recent_alerts": recent_alerts,
    "analytics_data": analytics_data,
    "memory": (current, peak)
}
