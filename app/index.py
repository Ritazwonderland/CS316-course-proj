from flask import render_template, Blueprint
from flask_login import current_user
from .models.product import Product
from .models.order_buy import OrderBuy  # Changed import
from datetime import datetime, timedelta

bp = Blueprint('index', __name__)

@bp.route('/')
def index():
    # get all available products for sale:
    products = Product.get_all(True)
    
    # if user is logged in, get their order history
    if current_user.is_authenticated:
        # Get orders from the last 30 days
        since = datetime.now() - timedelta(days=10)
        orders = OrderBuy.get_orders_since(current_user.id, since)  # Assumes you'll implement this method
    else:
        orders = None
    
    # render the page by adding information to the index.html file
    return render_template('index.html',
                           avail_products=products,
                           purchase_history=orders)  # Changed to orders
