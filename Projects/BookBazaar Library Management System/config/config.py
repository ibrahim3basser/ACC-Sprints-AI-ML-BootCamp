import os

class Config:
    # SQLite Configuration
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    SQLITE_DB_PATH = os.path.join(BASE_DIR, 'database', 'bookbazaar.db')
    
    # MongoDB Configuration
    MONGO_URI = 'mongodb://localhost:27017/'
    MONGO_DB_NAME = 'bookbazaar_reviews'