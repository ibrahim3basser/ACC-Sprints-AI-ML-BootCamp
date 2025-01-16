from datetime import datetime

class Review:
    """
    Review Model: Represents a book review (stored in MongoDB)
    Attributes:
        id (str): MongoDB ObjectId as string
        book_id (int): Reference to the book in SQLite
        user_id (int): Reference to the user in SQLite
        rating (int): Rating score (typically 1-5)
        comment (str): Review text
        date (datetime): Date and time of the review
    """
    def __init__(self, id, book_id, user_id, rating, comment, date=None):
        self.id = id
        self.book_id = book_id
        self.user_id = user_id
        self.rating = rating
        self.comment = comment
        self.date = date or datetime.utcnow()

    def to_dict(self):
        """
        Converts Review object to dictionary for JSON serialization
        Returns:
            dict: Dictionary representation of the review
        """
        return {
            'id': str(self.id),
            'book_id': self.book_id,
            'user_id': self.user_id,
            'rating': self.rating,
            'comment': self.comment,
            'date': self.date.isoformat()
        }

    @staticmethod
    def from_mongo(mongo_doc):
        """
        Creates a Review object from a MongoDB document
        Args:
            mongo_doc: MongoDB document containing review data
        Returns:
            Review: New Review instance with data from document
        """
        return Review(
            id=str(mongo_doc['_id']),
            book_id=mongo_doc['book_id'],
            user_id=mongo_doc['user_id'],
            rating=mongo_doc['rating'],
            comment=mongo_doc['comment'],
            date=mongo_doc.get('date', datetime.utcnow())
        )