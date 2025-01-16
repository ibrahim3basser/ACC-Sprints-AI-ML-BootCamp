class Stock:
    """
    Stock Model: Represents inventory levels for books
    Attributes:
        id (int): Unique identifier for the stock record
        book_id (int): Foreign key reference to the book
        quantity (int): Current quantity in stock
    """
    def __init__(self, id, book_id, quantity):
        self.id = id
        self.book_id = book_id
        self.quantity = quantity

    @staticmethod
    def from_db_row(row):
        """
        Creates a Stock object from a database row
        Args:
            row: SQLite row containing stock data
        Returns:
            Stock: New Stock instance with data from row
        """
        return Stock(
            id=row['id'],
            book_id=row['book_id'],
            quantity=row['quantity']
        )

    def to_dict(self):
        """
        Converts Stock object to dictionary for JSON serialization
        Returns:
            dict: Dictionary representation of the stock
        """
        return {
            'id': self.id,
            'book_id': self.book_id,
            'quantity': self.quantity
        }