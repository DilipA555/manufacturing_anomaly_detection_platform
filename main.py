from database.database_manager import DatabaseManager
from data.data_generator import DataGenerator
from data.data_ingestion import DataIngestion
from data.data_processor import DataProcessor



# test database connection and table creation
db = DatabaseManager()
db.connect()
db.create_tables()
db.insert_thresholds()
db.close()

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