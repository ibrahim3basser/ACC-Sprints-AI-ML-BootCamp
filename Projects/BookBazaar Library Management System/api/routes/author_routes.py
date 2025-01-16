from flask import Blueprint, jsonify, request
from app.services.author_service import AuthorService
from app.services.book_service import BookService

author_routes = Blueprint('author_routes', __name__)

@author_routes.route('/authors', methods=['GET'])
def get_authors():
    """
    Get all authors
    ---
    Endpoint: /authors
    Method: GET
    Query Parameters:
        - country (optional): Filter by country
        - sort (optional): Sort by field (name, country)
        - order (optional): Sort order (asc, desc)
    Returns:
        - 200: List of authors
        - 500: Server error
    """
    try:
        # Get query parameters
        country = request.args.get('country')
        sort = request.args.get('sort', 'name')
        order = request.args.get('order', 'asc')

        authors = AuthorService.get_all_authors()
        return jsonify([author.to_dict() for author in authors]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@author_routes.route('/authors/<int:author_id>', methods=['GET'])
def get_author(author_id):
    """
    Get a specific author by ID
    ---
    Endpoint: /authors/<id>
    Method: GET
    Parameters:
        - author_id: ID of the author to retrieve
    Returns:
        - 200: Author details with their books
        - 404: Author not found
        - 500: Server error
    """
    try:
        author = AuthorService.get_author_by_id(author_id)
        if author:
            # Get author's books
            books = BookService.get_books_by_author(author_id)
            response_data = author.to_dict()
            
            #response_data['books'] = [book.to_dict() for book in books]
            #response_data['total_books'] = len(books)
            return jsonify(response_data), 200
        return jsonify({'error': 'Author not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@author_routes.route('/authors', methods=['POST'])
def create_author():
    """
    Create a new author
    ---
    Endpoint: /authors
    Method: POST
    Request Body:
        - name (required): Author's name
        - country (required): Author's country
        - birthdate (optional): Author's birthdate (YYYY-MM-DD)
    Returns:
        - 201: Author created successfully
        - 400: Missing required fields
        - 500: Server error
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        if not all(field in data for field in ['name', 'country']):
            return jsonify({'error': 'Missing required fields'}), 400

        author_id = AuthorService.create_author(
            name=data['name'],
            country=data['country'],
            birthdate=data.get('birthdate')
        )
        return jsonify({
            'id': author_id,
            'message': 'Author created successfully'
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500