from flask import Blueprint, jsonify, request
from app.services.sale_service import SaleService
from app.services.book_service import BookService
from app.services.stock_service import StockService

sale_routes = Blueprint('sale_routes', __name__)

@sale_routes.route('/sales', methods=['POST'])
def create_sale():
    """
    Create a new sale
    ---
    Endpoint: /sales
    Method: POST
    Request Body:
        - book_id (required): ID of the book being sold
        - user_id (required): ID of the purchasing user
        - quantity (required): Number of books to purchase
    Returns:
        - 201: Sale created successfully
        - 400: Missing fields or insufficient stock
        - 404: Book not found
        - 500: Server error
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['book_id', 'user_id', 'quantity']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400

        # Check stock availability
        if not StockService.check_availability(data['book_id'], data['quantity']):
            return jsonify({'error': 'Insufficient stock'}), 400

        # Get book price
        book = BookService.get_book_by_id(data['book_id'])
        if not book:
            return jsonify({'error': 'Book not found'}), 404

        sale_id = SaleService.create_sale(
            book_id=data['book_id'],
            user_id=data['user_id'],
            quantity=data['quantity'],
            price_per_unit=book.price
        )
        return jsonify({
            'id': sale_id,
            'message': 'Sale created successfully'
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@sale_routes.route('/sales/user/<int:user_id>', methods=['GET'])
def get_user_sales(user_id):
    """
    Get all sales for a specific user
    ---
    Endpoint: /sales/user/<user_id>
    Method: GET
    Parameters:
        - user_id: ID of the user
    Returns:
        - 200: List of user's sales
        - 500: Server error
    """
    try:
        sales = SaleService.get_user_sales(user_id)
        return jsonify([sale.to_dict() for sale in sales]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500