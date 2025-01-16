from datetime import datetime

class Sale:
    """
    Sale Model: Represents a book sale transaction
    Attributes:
        id (int): Unique identifier for the sale
        book_id (int): Foreign key reference to the book
        user_id (int): Foreign key reference to the user
        quantity (int): Number of books sold
        sale_date (datetime): Date and time of the sale
        total_price (float): Total price of the sale
    """
    def __init__(self, id, book_id, user_id, quantity, sale_date, total_price):
        self.id = id
        self.book_id = book_id
        self.user_id = user_id
        self.quantity = quantity
        self.sale_date = sale_date
        self.total_price = total_price

    @staticmethod
    def from_db_row(row):
        """
        Creates a Sale object from a database row
        Args:
            row: SQLite row containing sale data
        Returns:
            Sale: New Sale instance with data from row
        """
        return Sale(
            id=row['id'],
            book_id=row['book_id'],
            user_id=row['user_id'],
            quantity=row['quantity'],
            sale_date=row['sale_date'],
            total_price=row['total_price']
        )

    def to_dict(self):
        """
        Converts Sale object to dictionary for JSON serialization
        Returns:
            dict: Dictionary representation of the sale
        """
        return {
            'id': self.id,
            'book_id': self.book_id,
            'user_id': self.user_id,
            'quantity': self.quantity,
            'sale_date': self.sale_date.isoformat() if isinstance(self.sale_date, datetime) else self.sale_date,
            'total_price': self.total_price
        }