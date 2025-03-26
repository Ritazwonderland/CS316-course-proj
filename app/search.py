from flask import render_template
from flask_login import current_user
import datetime

from .models.product import Product

from flask import Blueprint

from .models.product import Product

from flask import request

bp = Blueprint('search', __name__)

@bp.route('/search', methods=['GET'])
def search():
    search = request.args.get('search_term', default=None, type=str)
    category = request.args.get('category', default=None, type=str)
    search_products = Product.search(search, category)
    return render_template('most_expensive.html', products = search_products, search = search, category = category)

@bp.route('/get_product', methods=['GET'])
def get_product():
    product_id = request.args.get('product_id', default=None, type=int)
    search_product = Product.get(product_id)
    search_inventory = Product.getInventory(product_id)
    search_feedback = Product.getFeedback(product_id)

    print(search_feedback)

    return render_template('product_page.html', product = search_product, sellers = search_inventory, feedbacks = search_feedback)
