class Book:
    """
    Book Model: Represents a book in the library system
    Attributes:
        id (int): Unique identifier for the book
        title (str): Title of the book
        author_id (int): Foreign key reference to the author
        genre (str): Book genre/category
        published_year (int): Year the book was published
        price (float): Price of the book
    """
    def __init__(self, id, title, author_id, genre, published_year, price):
        self.id = id
        self.title = title
        self.author_id = author_id
        self.genre = genre
        self.published_year = published_year
        self.price = price

    @staticmethod
    def from_db_row(row):
        """
        Creates a Book object from a database row
        Args:
            row: SQLite row containing book data
        Returns:
            Book: New Book instance with data from row
        """
        return Book(
            id=row['id'],
            title=row['title'],
            author_id=row['author_id'],
            genre=row['genre'],
            published_year=row['published_year'],
            price=row['price']
        )

    def to_dict(self):
        """
        Converts Book object to dictionary for JSON serialization
        Returns:
            dict: Dictionary representation of the book
        """
        return {
            'id': self.id,
            'title': self.title,
            'author_id': self.author_id,
            'genre': self.genre,
            'published_year': self.published_year,
            'price': self.price
        }