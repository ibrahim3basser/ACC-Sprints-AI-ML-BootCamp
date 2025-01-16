from datetime import datetime
from bson import ObjectId
from app.services.mongo_service import MongoService
from app.models.review import Review

class ReviewService:
    """
    Service class for handling book reviews
    Manages reviews stored in MongoDB
    """

    @staticmethod
    def create_review(book_id, user_id, rating, comment):
        """
        Creates a new book review
        Args:
            book_id (int): ID of the book being reviewed
            user_id (int): ID of the reviewing user
            rating (int): Rating score (1-5)
            comment (str): Review text
        Returns:
            str: ID of the created review
        """
        db = MongoService.get_db()
        try:
            result = db.reviews.insert_one({
                'book_id': book_id,
                'user_id': user_id,
                'rating': rating,
                'comment': comment,
                'date': datetime.utcnow()
            })
            return str(result.inserted_id)
        except Exception as e:
            print(f"Error creating review: {e}")
            return None

    @staticmethod
    def get_book_reviews(book_id):
        """
        Retrieves all reviews for a specific book
        Args:
            book_id (int): ID of the book
        Returns:
            list: List of Review objects
        """
        db = MongoService.get_db()
        try:
            reviews = db.reviews.find({'book_id': book_id})
            return [Review.from_mongo(review) for review in reviews]
        except Exception as e:
            print(f"Error getting reviews: {e}")
            return []


    @staticmethod
    def delete_review(review_id):
        """
        Deletes a review by ID
        Args:
            review_id (str): ID of the review to delete
        Returns:
            bool: True if deletion was successful
        """
        db = MongoService.get_db()
        try:
            result = db.reviews.delete_one({'_id': ObjectId(review_id)})
            return result.deleted_count > 0
        except Exception as e:
            print(f"Error deleting review: {e}")
            return False
        
        
    @staticmethod
    def update_review(review_id, rating=None, comment=None):
        """
        Updates an existing review
        Args:
            review_id (str): ID of the review to update
            rating (int, optional): New rating
            comment (str, optional): New comment
        Returns:
            bool: True if update successful
        """
        db = MongoService.get_db()
        try:
            update_data = {
                'updated_at': datetime.utcnow()
            }
            if rating is not None:
                update_data['rating'] = rating
            if comment is not None:
                update_data['comment'] = comment

            result = db.reviews.update_one(
                {'_id': ObjectId(review_id)},
                {'$set': update_data}
            )
            return result.modified_count > 0
        except Exception as e:
            print(f"Error updating review: {e}")
            return False