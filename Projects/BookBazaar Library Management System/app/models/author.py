class Author:
    """
    Author Model: Represents an author in the library system
    Attributes:
        id (int): Unique identifier for the author
        name (str): Author's full name
        country (str): Author's country of origin
        birthdate (date): Author's date of birth
    """
    def __init__(self, id, name, country, birthdate):
        self.id = id
        self.name = name
        self.country = country
        self.birthdate = birthdate

    @staticmethod
    def from_db_row(row):
        """
        Creates an Author object from a database row
        Args:
            row: SQLite row containing author data
        Returns:
            Author: New Author instance with data from row
        """
        return Author(
            id=row['id'],
            name=row['name'],
            country=row['country'],
            birthdate=row['birthdate']
        )

    def to_dict(self):
        """
        Converts Author object to dictionary for JSON serialization
        Returns:
            dict: Dictionary representation of the author
        """
        return {
            'id': self.id,
            'name': self.name,
            'country': self.country,
            'birthdate': self.birthdate
        }