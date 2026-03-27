import mysql.connector
from mysql.connector import Error
from config.config import Config


class DatabaseManager:
    """Handles database connection and operations"""

    def __init__(self):
        """Initialize database connection"""
        self.connection = None

    def connect(self):
        """Connect to MySQL database"""
        try:
            self.connection = mysql.connector.connect(
                host=Config.DB_HOST,
                user=Config.DB_USER,
                password=Config.DB_PASSWORD,
                database=Config.DB_NAME
            )

        except Error as e:
            print(f"Error while connecting: {e}")

    def create_tables(self):
        """Create required tables if not present"""
        try:
            cursor = self.connection.cursor()

            # sector thresholds table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS sector_thresholds (
                    sector VARCHAR(50) PRIMARY KEY,
                    temperature FLOAT,
                    vibration FLOAT,
                    pressure FLOAT,
                    energy FLOAT,
                    production FLOAT
                )
            """)

            # machine data table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS machine_data (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    machine_id VARCHAR(50),
                    sector VARCHAR(50),
                    temperature FLOAT,
                    vibration FLOAT,
                    pressure FLOAT,
                    energy FLOAT,
                    production FLOAT,
                    status VARCHAR(20),
                    timestamp DATETIME
                )
            """)

            # anomaly log table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS anomaly_log (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    machine_id VARCHAR(50),
                    sector VARCHAR(50),
                    anomaly_type VARCHAR(50),
                    value FLOAT,
                    timestamp DATETIME
                )
            """)

            self.connection.commit()

        except Error as e:
            print(f"Error while creating tables: {e}")

    def insert_thresholds(self):
        """Insert default thresholds into table"""
        try:
            cursor = self.connection.cursor()

            for sector, values in Config.DEFAULT_THRESHOLDS.items():
                cursor.execute("""
                    INSERT INTO sector_thresholds 
                    (sector, temperature, vibration, pressure, energy, production)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                    temperature=VALUES(temperature),
                    vibration=VALUES(vibration),
                    pressure=VALUES(pressure),
                    energy=VALUES(energy),
                    production=VALUES(production)
                """, (
                    sector,
                    values["temperature"],
                    values["vibration"],
                    values["pressure"],
                    values["energy"],
                    values["production"]
                ))

            self.connection.commit()

        except Error as e:
            print(f"Error inserting thresholds: {e}")

    def insert_anomalies(self, alerts):
        """Insert alert data into anomaly_log table"""
        try:
            cursor = self.connection.cursor()

            for alert in alerts:
                cursor.execute("""
                    INSERT INTO anomaly_log (machine_id, sector, anomaly_type, value, timestamp)
                    VALUES (%s, %s, %s, %s, %s)
                """, (
                    alert["machine_id"],
                    alert["sector"],
                    alert["parameter"],   # maps to anomaly_type
                    alert["value"],
                    alert["timestamp"]
                ))

            self.connection.commit()

        except Error as e:
            print(f"Error inserting alerts: {e}")

    def fetch_anomalies(self, limit=10):
        """Fetch recent anomaly records from database"""
        try:
            cursor = self.connection.cursor(dictionary=True)

            cursor.execute(f"""
                SELECT machine_id, sector, anomaly_type, value, timestamp
                FROM anomaly_log
                ORDER BY timestamp DESC
                LIMIT {limit}
            """)

            results = cursor.fetchall()
            return results

        except Error as e:
            print(f"Error fetching data: {e}")
            return []

    def close(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()