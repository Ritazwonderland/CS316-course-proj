from flask import Flask
from .config import Config
from .db import DB
from app.models.user import User
from app.login_manager import login  # Import the login manager
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

db = None  # Global variable to hold the DB instance
login_manager = LoginManager()
login_manager.login_view = 'users.login'

bootstrap = Bootstrap()

def create_app():
    global db
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize Bootstrap
    bootstrap.init_app(app)

    # Initialize the database and attach it to the app
    db = DB(app)
    app.db = db
    login.init_app(app)
    login_manager.init_app(app)

    from .index import bp as index_bp
    app.register_blueprint(index_bp)

    from app.routes import bp as users_bp
    app.register_blueprint(users_bp, url_prefix='/users')

    from .inventory import bp as inventory_bp
    app.register_blueprint(inventory_bp)

    from .order_history import bp as order_history_bp  
    app.register_blueprint(order_history_bp)

    from .feedback import bp as feedback_bp
    app.register_blueprint(feedback_bp)

    # Register new blueprints for cart_items, orders, and order_items
    from .cart_items import bp as cart_items_bp
    app.register_blueprint(cart_items_bp)

    from .orders import bp as orders_bp
    app.register_blueprint(orders_bp)

    from .order_items import bp as order_items_bp
    app.register_blueprint(order_items_bp)

    # Set the db object in the db module
    from . import db as db_module
    db_module.db = db

    from .search import bp as search_bp
    app.register_blueprint(search_bp)
    

    from .add_product import bp as add_product_bp
    app.register_blueprint(add_product_bp)
    return app

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)
