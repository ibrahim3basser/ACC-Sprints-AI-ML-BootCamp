import sqlite3
from contextlib import contextmanager
from config.config import Config

class SQLiteService:
    """
    Base service for SQLite database operations
    Provides connection management and database initialization
    """
    
    @staticmethod
    @contextmanager
    def get_connection():
        """
        Context manager for database connections
        Ensures proper connection handling and cleanup
        Yields:
            sqlite3.Connection: Database connection object
        """
        conn = sqlite3.connect(Config.SQLITE_DB_PATH)
        conn.row_factory = sqlite3.Row  # Enable row name access
        try:
            yield conn
        finally:
            conn.close()

    @staticmethod
    def init_db():
        """
        Initializes the database with schema
        Creates all necessary tables if they don't exist
        """
        #D:/ACC_Sprints_AI_ML_BootCamp/Capstone_projects/Cap2_BookBazaar/database
        with open('D:/ACC_Sprints_AI_ML_BootCamp/Capstone_projects/Cap2_BookBazaar/database/schema.sql', 'r') as f:
            schema = f.read()
        with SQLiteService.get_connection() as conn:
            conn.executescript(schema)
            conn.commit()