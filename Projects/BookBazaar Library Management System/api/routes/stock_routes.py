from flask import Blueprint, jsonify, request
from app.services.stock_service import StockService
from app.services.book_service import BookService

stock_routes = Blueprint('stock_routes', __name__)

@stock_routes.route('/stock/<int:book_id>', methods=['GET'])
def get_stock(book_id):
    """
    Get stock level for a specific book
    ---
    Endpoint: /stock/<book_id>
    Method: GET
    Parameters:
        - book_id: ID of the book
    Returns:
        - 200: Stock details
        - 404: Stock not found
        - 500: Server error
    """
    try:
        stock = StockService.get_stock_by_book_id(book_id)
        if stock:
            return jsonify(stock.to_dict()), 200
        return jsonify({'error': 'Stock not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@stock_routes.route('/stock/<int:book_id>', methods=['PUT'])
def update_stock(book_id):
    """
    Update stock level for a book
    ---
    Endpoint: /stock/<book_id>
    Method: PUT
    Parameters:
        - book_id: ID of the book
    Request Body:
        - quantity (required): New stock quantity
    Returns:
        - 200: Stock updated successfully
        - 400: Missing quantity
        - 404: Stock not found
        - 500: Server error
    """
    try:
        data = request.get_json()
        if 'quantity' not in data:
            return jsonify({'error': 'Quantity is required'}), 400

        success = StockService.update_stock(
            book_id=book_id,
            quantity=data['quantity']
        )
        if success:
            return jsonify({'message': 'Stock updated successfully'}), 200
        return jsonify({'error': 'Stock not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500