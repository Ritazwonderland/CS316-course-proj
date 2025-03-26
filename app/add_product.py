from flask import render_template
from flask_login import current_user
import datetime

from .models.product import Product

from flask import Blueprint

from .models.product import Product

from flask import request

bp = Blueprint('add_product', __name__)

@bp.route('/add_product', methods=['POST'])
def add_product():
    product_name = request.form.get('product-name')
    description = request.form.get('product-description')
    price = request.form.get('product-price')
    category = request.form.get('product-category')
    Product.add_product(product_name, price, description, NULL, category, True)

@bp.route('/update_product', methods=['POST'])
def update_product():
    product_name = request.form.get('product_name')
    description = request.form.get('description')
    price = request.form.get('price')
    category = request.form.get('category')