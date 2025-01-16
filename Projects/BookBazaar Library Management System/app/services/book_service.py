from app.services.sqlite_service import SQLiteService
from app.models.book import Book

class BookService:
    """
    Service class for handling book-related operations
    Manages CRUD operations for books in SQLite database
    """

    @staticmethod
    def get_all_books():
        """
        Retrieves all books from the database
        Returns:
            list: List of Book objects
        """
        with SQLiteService.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM Books')
            return [Book.from_db_row(row) for row in cursor.fetchall()]

    @staticmethod
    def get_book_by_id(book_id):
        """
        Retrieves a specific book by ID
        Args:
            book_id (int): ID of the book to retrieve
        Returns:
            Book: Book object if found, None otherwise
        """
        with SQLiteService.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM Books WHERE id = ?', (book_id,))
            row = cursor.fetchone()
            return Book.from_db_row(row) if row else None
        
    @staticmethod
    def get_books_by_author(author_id):
        """
        Retrieves a  books by author ID
        Args:
            author_id (int): ID of author to retrieve
        Returns:
            Books: Book object if found, None otherwise
        """
        with SQLiteService.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM Books WHERE author_id = ?', (author_id,))
            row = cursor.fetchone()
            return Book.from_db_row(row) if row else None

    @staticmethod
    def create_book(title, author_id, genre, published_year, price):
        """
        Creates a new book in the database
        Args:
            title (str): Book title
            author_id (int): ID of the author
            genre (str): Book genre
            published_year (int): Year of publication
            price (float): Book price
        Returns:
            int: ID of the created book
        """
        with SQLiteService.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO Books (title, author_id, genre, published_year, price)
                VALUES (?, ?, ?, ?, ?)
            ''', (title, author_id, genre, published_year, price))
            conn.commit()
            return cursor.lastrowid

    @staticmethod
    def update_book(book_id, title=None, genre=None, price=None):
        """
        Updates an existing book's information
        Args:
            book_id (int): ID of the book to update
            title (str, optional): New title
            genre (str, optional): New genre
            price (float, optional): New price
        Returns:
            bool: True if update successful, False otherwise
        """
        with SQLiteService.get_connection() as conn:
            cursor = conn.cursor()
            updates = []
            values = []
            if title is not None:
                updates.append('title = ?')
                values.append(title)
            if genre is not None:
                updates.append('genre = ?')
                values.append(genre)
            if price is not None:
                updates.append('price = ?')
                values.append(price)
            
            if not updates:
                return False

            values.append(book_id)
            query = f'''
                UPDATE Books 
                SET {', '.join(updates)}
                WHERE id = ?
            '''
            cursor.execute(query, values)
            conn.commit()
            return cursor.rowcount > 0

    @staticmethod
    def delete_book(book_id):
        """
        Deletes a book from the database
        Args:
            book_id (int): ID of the book to delete
        Returns:
            bool: True if deletion successful, False otherwise
        """
        with SQLiteService.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM Books WHERE id = ?', (book_id,))
            conn.commit()
            return cursor.rowcount > 0