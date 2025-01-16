from pymongo import MongoClient
from bson import ObjectId
from config.config import Config

class MongoService:
    """
    Base service for MongoDB operations
    Provides connection management and database initialization
    """
    
    @staticmethod
    def get_db():
        """
        Gets MongoDB database connection
        Returns:
            pymongo.database.Database: MongoDB database instance
        """
        client = MongoClient(Config.MONGO_URI)
        return client[Config.MONGO_DB_NAME]

    @staticmethod
    def init_db():
        """
        Initializes MongoDB database
        Creates necessary indexes for better query performance
        """
        db = MongoService.get_db()
        # Create indexes for common queries
        db.reviews.create_index([("book_id", 1)])  # Index for book lookups
        db.reviews.create_index([("user_id", 1)])  # Index for user lookups