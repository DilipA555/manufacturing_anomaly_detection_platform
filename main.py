from database.database_manager import DatabaseManager
from data.data_generator import DataGenerator


# test database connection and table creation
db = DatabaseManager()
db.connect()
db.create_tables()
db.insert_thresholds()
db.close()

# test data generation
generator = DataGenerator()
generator.generate_data()