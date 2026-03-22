import mysql.connector
from mysql.connector import Error
from config.config import Config


class DatabaseManager:
    """Handles database connection and operations"""

    def _init_(self):
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

            if self.connection.is_connected():
                print("Connected to database")

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
            print("Tables created")

        except Error as e:
            print(f"Error while creating tables: {e}")

    def close(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Database connection closed")