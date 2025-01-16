from flask import Blueprint, jsonify, request
from datetime import datetime 
from app.services.book_service import BookService
from app.services.author_service import AuthorService
from app.services.stock_service import StockService

book_routes = Blueprint('book_routes', __name__)

@book_routes.route('/books', methods=['GET'])
def get_books():
    """
    Get all books
    ---
    Endpoint: /books
    Method: GET
    Query Parameters:
        - genre (optional): Filter books by genre
        - sort (optional): Sort by field (title, price)
        - order (optional): Sort order (asc, desc)
    Returns:
        - 200: List of books
        - 500: Server error
    """
    try:
        # Get query parameters for filtering and sorting
        genre = request.args.get('genre')
        sort = request.args.get('sort', 'title')
        order = request.args.get('order', 'asc')

        books = BookService.get_all_books()
        return jsonify([book.to_dict() for book in books]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@book_routes.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    """
    Get a specific book by ID
    ---
    Endpoint: /books/<id>
    Method: GET
    Parameters:
        - book_id: ID of the book to retrieve
    Returns:
        - 200: Book details with stock and author information
        - 404: Book not found
        - 500: Server error
    """
    try:
        book = BookService.get_book_by_id(book_id)
        if book:
            # Get additional book information
            stock = StockService.get_stock_by_book_id(book_id)
            author = AuthorService.get_author_by_id(book.author_id)
            
            # Prepare response data
            response_data = book.to_dict()
            response_data['stock_quantity'] = stock.quantity if stock else 0
            response_data['author'] = author.to_dict() if author else None
            
            return jsonify(response_data), 200
        return jsonify({'error': 'Book not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@book_routes.route('/books', methods=['POST'])
def create_book():
    """
    Create a new book
    ---
    Endpoint: /books
    Method: POST
    Request Body:
        - title (required): Book title
        - author_id (required): ID of the author here assume that i have ui and  frontend that will provide the author_id  
            let say i have selector have names of authors and each author has id so i will select the author and get the id of the author 
        - genre (optional): Book genre
        - published_year (optional): Year of publication
        - price (required): Book price
    Returns:
        - 201: Book created successfully
        - 400: Missing required fields
        - 404: Author not found
        - 500: Server error
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['title', 'author_id', 'price']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        # Verify author exists
        author = AuthorService.get_author_by_id(data['author_id'])
        if not author:
            return jsonify({'error': 'Author not found'}), 404

        # Create book
        book_id = BookService.create_book(
            title=data['title'],
            author_id=data['author_id'],
            genre=data.get('genre'),
            published_year=data.get('published_year'),
            price=data['price']
        )

        # Initialize stock
        StockService.create_stock(book_id, quantity=0)

        return jsonify({
            'id': book_id,
            'message': 'Book created successfully'
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@book_routes.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    """
    Update an existing book
    ---
    Endpoint: /books/<id>
    Method: PUT
    Parameters:
        - book_id: ID of the book to update
    Request Body:
        - title (optional): New title
        - genre (optional): New genre
        - price (optional): New price
    Returns:
        - 200: Book updated successfully
        - 404: Book not found
        - 500: Server error
    """
    try:
        data = request.get_json()
        
        success = BookService.update_book(
            book_id=book_id,
            title=data.get('title'),
            genre=data.get('genre'),
            price=data.get('price')
        )

        if success:
            return jsonify({'message': 'Book updated successfully'}), 200
        return jsonify({'error': 'Book not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@book_routes.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    """
    Delete a book
    ---
    Endpoint: /books/<id>
    Method: DELETE
    Parameters:
        - book_id: ID of the book to delete
    Returns:
        - 200: Book deleted successfully
        - 404: Book not found
        - 500: Server error
    """
    try:
        success = BookService.delete_book(book_id)
        if success:
            
            return jsonify({'message': 'Book deleted successfully'}), 200
        return jsonify({'error': 'Book not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@book_routes.route('/books/search', methods=['GET'])
def search_books():
    """
    Search books by title or genre
    ---
    Endpoint: /books/search
    Method: GET
    Query Parameters:
        - query: Search term
        - field: Field to search (title, genre)
    Returns:
        - 200: List of matching books
        - 400: Missing search query
        - 500: Server error
    """
    try:
        query = request.args.get('query')
        field = request.args.get('field', 'title')

        if not query:
            return jsonify({'error': 'Search query is required'}), 400

        books = BookService.search_books(query, field)
        return jsonify([book.to_dict() for book in books]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500