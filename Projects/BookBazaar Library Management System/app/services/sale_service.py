from datetime import datetime
from app.services.sqlite_service import SQLiteService
from app.services.stock_service import StockService
from app.models.sale import Sale

class SaleService:
    """
    Service class for handling sales operations
    Manages book sales and updates stock accordingly
    """

    @staticmethod
    def create_sale(book_id, user_id, quantity, price_per_unit):
        """
        Creates a new sale transaction
        Args:
            book_id (int): ID of the book being sold
            user_id (int): ID of the purchasing user
            quantity (int): Number of books being purchased
            price_per_unit (float): Price per book
        Returns:
            int: ID of the created sale record
        Raises:
            ValueError: If insufficient stock
        """
        if not StockService.check_availability(book_id, quantity):
            raise ValueError("Insufficient stock")

        total_price = quantity * price_per_unit
        
        with SQLiteService.get_connection() as conn:
            cursor = conn.cursor()
            try:
                # Create sale record
                cursor.execute('''
                    INSERT INTO Sales (book_id, user_id, quantity, total_price)
                    VALUES (?, ?, ?, ?)
                ''', (book_id, user_id, quantity, total_price))
                
                # Update stock
                cursor.execute('''
                    UPDATE Stock 
                    SET quantity = quantity - ?
                    WHERE book_id = ?
                ''', (quantity, book_id))
                
                conn.commit()
                return cursor.lastrowid
            except Exception as e:
                conn.rollback()
                raise e

    @staticmethod
    def get_user_sales(user_id):
        """
        Retrieves all sales for a specific user
        Args:
            user_id (int): ID of the user
        Returns:
            list: List of Sale objects
        """
        with SQLiteService.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT s.*, b.title 
                FROM Sales s
                JOIN Books b ON s.book_id = b.id
                WHERE s.user_id = ?
            ''', (user_id,))
            return [Sale.from_db_row(row) for row in cursor.fetchall()]