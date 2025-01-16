from flask import Flask
from api.routes.book_routes import book_routes
from api.routes.author_routes import author_routes
from api.routes.stock_routes import stock_routes
from api.routes.sale_routes import sale_routes
from api.routes.landing import landing
from api.routes.review_routes import review_routes  # Added for MongoDB reviews
from app.services.sqlite_service import SQLiteService
from app.services.mongo_service import MongoService  # Added MongoDB service
import os

#app = Flask(__name__)
def create_app():
    app = Flask(__name__)
    
    # Register blueprints
    app.register_blueprint(book_routes)
    app.register_blueprint(author_routes)
    app.register_blueprint(stock_routes)
    app.register_blueprint(sale_routes)
    app.register_blueprint(review_routes)  # Added reviews blueprint
    app.register_blueprint(landing)   
    # Initialize SQLite database if it doesn't exist
    if not os.path.exists('database/bookbazaar.db'):
        SQLiteService.init_db()
    
    # Initialize MongoDB connection
    try:
        MongoService.init_db()
    except Exception as e:
        print(f"Warning: MongoDB initialization failed: {e}")
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)