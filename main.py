from database.database_manager import DatabaseManager

# test database connection and table creation
db = DatabaseManager()
db.connect()
db.create_tables()
db.insert_thresholds()
db.close()