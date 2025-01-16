from app.services.sqlite_service import SQLiteService
from app.models.author import Author

class AuthorService:
    """
    Service class for handling author-related operations
    Manages CRUD operations for authors in SQLite database
    """

    @staticmethod
    def get_all_authors():
        """
        Retrieves all authors from the database
        Returns:
            list: List of Author objects
        """
        with SQLiteService.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM Authors')
            return [Author.from_db_row(row) for row in cursor.fetchall()]

    @staticmethod
    def get_author_by_id(author_id):
        """
        Retrieves a specific author by ID
        Args:
            author_id (int): ID of the author to retrieve
        Returns:
            Author: Author object if found, None otherwise
        """
        with SQLiteService.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM Authors WHERE id = ?', (author_id,))
            row = cursor.fetchone()
            return Author.from_db_row(row) if row else None

    @staticmethod
    def create_author(name, country, birthdate):
        """
        Creates a new author in the database
        Args:
            name (str): Author's name
            country (str): Author's country
            birthdate (str): Author's birthdate
        Returns:
            int: ID of the created author
        """
        with SQLiteService.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO Authors (name, country, birthdate)
                VALUES (?, ?, ?)
            ''', (name, country, birthdate))
            conn.commit()
            return cursor.lastrowid

    @staticmethod
    def update_author(author_id, name=None, country=None):
        """
        Updates an existing author's information
        Args:
            author_id (int): ID of the author to update
            name (str, optional): New name
            country (str, optional): New country
        Returns:
            bool: True if update successful, False otherwise
        """
        with SQLiteService.get_connection() as conn:
            cursor = conn.cursor()
            updates = []
            values = []
            if name is not None:
                updates.append('name = ?')
                values.append(name)
            if country is not None:
                updates.append('country = ?')
                values.append(country)
            
            if not updates:
                return False

            values.append(author_id)
            query = f'''
                UPDATE Authors 
                SET {', '.join(updates)}
                WHERE id = ?
            '''
            cursor.execute(query, values)
            conn.commit()
            return cursor.rowcount > 0