from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user
from .models.order_buy import OrderBuy  

bp = Blueprint('orders', __name__)

@bp.route('/orders', methods=['GET'])
def get_orders():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))  # Redirect to login if not authenticated

    orders = OrderBuy.get_all_by_user(current_user.id)  # Get the orders
    return render_template('orders.html', orders=orders)  # Render orders template

@bp.route('/orders/create', methods=['POST'])
def create_order():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    order_id = OrderBuy.add(current_user.id)  # Use OrderBuy.add method to create an order
    if order_id:
        flash('Order created successfully.')
        return redirect(url_for('orders.get_orders'))

    flash('Failed to create order.')
    return redirect(url_for('orders.get_orders'))


