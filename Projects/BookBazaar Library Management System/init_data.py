import sys
from pathlib import Path
from datetime import datetime

# Add the project root directory to Python path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

from app.services.sqlite_service import SQLiteService
from app.services.author_service import AuthorService
from app.services.book_service import BookService
from app.services.stock_service import StockService
from app.services.mongo_service import MongoService

def init_sample_data():
    """
    Initialize the database with sample data
    This function:
    1. Creates the database schema
    2. Adds sample authors
    3. Adds sample books
    4. Sets up initial stock levels
    5. Initializes MongoDB for reviews
    """
    try:
        print("Starting database initialization...")

        # Initialize SQLite database schema
        print("Creating database schema...")
        SQLiteService.init_db()

        # Initialize MongoDB
        print("Initializing MongoDB...")
        MongoService.init_db()

        # Create sample authors
        print("Creating sample authors...")
        authors_data = [
            {
                "name": "George Orwell",
                "country": "United Kingdom",
                "birthdate": "1903-06-25"
            },
            {
                "name": "J.K. Rowling",
                "country": "United Kingdom",
                "birthdate": "1965-07-31"
            },
            {
                "name": "Ernest Hemingway",
                "country": "United States",
                "birthdate": "1899-07-21"
            },
            {
                "name": "Agatha Christie",
                "country": "United Kingdom",
                "birthdate": "1890-09-15"
            }
        ]

        author_ids = {}
        for author_data in authors_data:
            author_id = AuthorService.create_author(
                name=author_data["name"],
                country=author_data["country"],
                birthdate=author_data["birthdate"]
            )
            author_ids[author_data["name"]] = author_id
            print(f"Created author: {author_data['name']}")

        # Create sample books
        print("\nCreating sample books...")
        books_data = [
            {
                "title": "1984",
                "author": "George Orwell",
                "genre": "Dystopian",
                "published_year": 1949,
                "price": 9.99,
                "initial_stock": 10
            },
            {
                "title": "Animal Farm",
                "author": "George Orwell",
                "genre": "Political Satire",
                "published_year": 1945,
                "price": 8.99,
                "initial_stock": 15
            },
            {
                "title": "Harry Potter and the Philosopher's Stone",
                "author": "J.K. Rowling",
                "genre": "Fantasy",
                "published_year": 1997,
                "price": 14.99,
                "initial_stock": 20
            },
            {
                "title": "Harry Potter and the Chamber of Secrets",
                "author": "J.K. Rowling",
                "genre": "Fantasy",
                "published_year": 1998,
                "price": 14.99,
                "initial_stock": 18
            },
            {
                "title": "The Old Man and the Sea",
                "author": "Ernest Hemingway",
                "genre": "Literary Fiction",
                "published_year": 1952,
                "price": 11.99,
                "initial_stock": 12
            },
            {
                "title": "Murder on the Orient Express",
                "author": "Agatha Christie",
                "genre": "Mystery",
                "published_year": 1934,
                "price": 10.99,
                "initial_stock": 15
            }
        ]

        for book_data in books_data:
            # Create book
            book_id = BookService.create_book(
                title=book_data["title"],
                author_id=author_ids[book_data["author"]],
                genre=book_data["genre"],
                published_year=book_data["published_year"],
                price=book_data["price"]
            )
            
            # Initialize stock
            StockService.create_stock(
                book_id=book_id,
                quantity=book_data["initial_stock"]
            )
            
            print(f"Created book: {book_data['title']} with initial stock: {book_data['initial_stock']}")

        print("\nDatabase initialization completed successfully!")
        print("\nSummary:")
        print(f"- Authors created: {len(authors_data)}")
        print(f"- Books created: {len(books_data)}")
        print("- Stock levels initialized for all books")
        print("\nYou can now start using the BookBazaar API!")

    except Exception as e:
        print(f"\nError during database initialization: {str(e)}")
        print("Database initialization failed. Please check the error message above.")
        # Optionally, you might want to clean up any partial data that was created
        print("You may need to delete the database file and try again.")
        sys.exit(1)

def verify_initialization():
    """
    Verify that the database was initialized correctly
    Performs basic checks on the created data
    """
    try:
        print("\nVerifying database initialization...")
        
        # Check authors
        authors = AuthorService.get_all_authors()
        print(f"Found {len(authors)} authors")

        # Check books
        books = BookService.get_all_books()
        print(f"Found {len(books)} books")

        # Check stock
        for book in books:
            stock = StockService.get_stock_by_book_id(book.id)
            if stock:
                print(f"Stock for '{book.title}': {stock.quantity}")
            else:
                print(f"Warning: No stock found for '{book.title}'")

        print("\nVerification completed!")
        return True

    except Exception as e:
        print(f"Verification failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("BookBazaar Database Initialization")
    print("=================================")
    
    # Check if database file already exists
    db_path = Path("database/bookbazaar.db")
    if db_path.exists():
        response = input("Database file already exists. Do you want to reinitialize? (y/N): ")
        if response.lower() != 'y':
            print("Initialization cancelled.")
            sys.exit(0)
        
    # Initialize database
    init_sample_data()
    
    # Verify initialization
    if verify_initialization():
        print("\nDatabase is ready to use!")
    else:
        print("\nWarning: Database verification failed!")