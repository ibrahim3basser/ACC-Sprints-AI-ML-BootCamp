from app.services.sqlite_service import SQLiteService
from app.models.stock import Stock

class StockService:
    """
    Service class for handling inventory stock operations
    Manages stock levels for books in the system
    """

    @staticmethod
    def get_stock_by_book_id(book_id):
        """
        Gets current stock level for a specific book
        Args:
            book_id (int): ID of the book
        Returns:
            Stock: Stock object if found, None otherwise
        """
        with SQLiteService.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM Stock WHERE book_id = ?', (book_id,))
            row = cursor.fetchone()
            return Stock.from_db_row(row) if row else None

    @staticmethod
    def update_stock(book_id, quantity):
        """
        Updates stock quantity for a book
        Args:
            book_id (int): ID of the book
            quantity (int): New quantity value
        Returns:
            bool: True if update successful, False otherwise
        """
        with SQLiteService.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE Stock 
                SET quantity = ?
                WHERE book_id = ?
            ''', (quantity, book_id))
            conn.commit()
            return cursor.rowcount > 0

    @staticmethod
    def create_stock(book_id, quantity):
        """
        Creates initial stock entry for a book
        Args:
            book_id (int): ID of the book
            quantity (int): Initial quantity
        Returns:
            int: ID of the created stock record
        """
        with SQLiteService.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO Stock (book_id, quantity)
                VALUES (?, ?)
            ''', (book_id, quantity))
            conn.commit()
            return cursor.lastrowid

    @staticmethod
    def check_availability(book_id, required_quantity):
        """
        Checks if enough stock is available for a purchase
        Args:
            book_id (int): ID of the book
            required_quantity (int): Quantity needed
        Returns:
            bool: True if sufficient stock available
        """
        stock = StockService.get_stock_by_book_id(book_id)
        return stock and stock.quantity >= required_quantity