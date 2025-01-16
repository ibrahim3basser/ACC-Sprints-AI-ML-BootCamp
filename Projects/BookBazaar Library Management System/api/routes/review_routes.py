from flask import Blueprint, jsonify, request
from app.services.review_service import ReviewService
from app.services.book_service import BookService

review_routes = Blueprint('review_routes', __name__)

@review_routes.route('/books/<int:book_id>/reviews', methods=['GET'])
def get_book_reviews(book_id):
    """
    Get all reviews for a specific book
    ---
    Endpoint: /books/<book_id>/reviews
    Method: GET
    Parameters:
        - book_id: ID of the book
    Returns:
        - 200: List of reviews
        - 404: Book not found
        - 500: Server error
    """
    try:
        # Verify book exists
        book = BookService.get_book_by_id(book_id)
        if not book:
            return jsonify({'error': 'Book not found'}), 404

        reviews = ReviewService.get_book_reviews(book_id)
        return jsonify([review.to_dict() for review in reviews]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@review_routes.route('/books/<int:book_id>/reviews', methods=['POST'])
def create_review(book_id):
    """
    Create a new review for a book
    ---
    Endpoint: /books/<book_id>/reviews
    Method: POST
    Parameters:
        - book_id: ID of the book
    Request Body:
        - user_id (required): ID of the reviewing user
        - rating (required): Rating score (1-5)
        - comment (required): Review text
    Returns:
        - 201: Review created successfully
        - 400: Missing required fields
        - 404: Book not found
        - 500: Server error
    """
    try:
        # Verify book exists
        book = BookService.get_book_by_id(book_id)
        if not book:
            return jsonify({'error': 'Book not found'}), 404

        data = request.get_json()
        required_fields = ['user_id', 'rating', 'comment']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400

        # Validate rating range
        if not 1 <= data['rating'] <= 5:
            return jsonify({'error': 'Rating must be between 1 and 5'}), 400

        review_id = ReviewService.create_review(
            book_id=book_id,
            user_id=data['user_id'],
            rating=data['rating'],
            comment=data['comment']
        )
        return jsonify({
            'id': review_id,
            'message': 'Review created successfully'
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@review_routes.route('/reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    """
    Update an existing review
    ---
    Endpoint: /reviews/<review_id>
    Method: PUT
    Parameters:
        - review_id: ID of the review
    Request Body:
        - rating (optional): New rating score (1-5)
        - comment (optional): New review text
    Returns:
        - 200: Review updated successfully
        - 400: Invalid rating
        - 404: Review not found
        - 500: Server error
    """
    try:
        data = request.get_json()
        
        # Validate rating if provided
        if 'rating' in data and not 1 <= data['rating'] <= 5:
            return jsonify({'error': 'Rating must be between 1 and 5'}), 400

        success = ReviewService.update_review(
            review_id=review_id,
            rating=data.get('rating'),
            comment=data.get('comment')
        )
        if success:
            return jsonify({'message': 'Review updated successfully'}), 200
        return jsonify({'error': 'Review not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@review_routes.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    """
    Delete a review
    ---
    Endpoint: /reviews/<review_id>
    Method: DELETE
    Parameters:
        - review_id: ID of the review to delete
    Returns:
        - 200: Review deleted successfully
        - 404: Review not found
        - 500: Server error
    """
    try:
        success = ReviewService.delete_review(review_id)
        if success:
            return jsonify({'message': 'Review deleted successfully'}), 200
        return jsonify({'error': 'Review not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500