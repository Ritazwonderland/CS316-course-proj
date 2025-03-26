from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user
from .models.order_item import OrderItem  # Assuming you have an OrderItem model

bp = Blueprint('order_items', __name__)

@bp.route('/order_items/<int:order_id>', methods=['GET'])
def get_order_items(order_id):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    items = OrderItem.get_by_order_id(order_id)  # Fetch all items in the order
    if not items:
        flash('No items found for this order.', 'warning')
        return redirect(url_for('users.account_dashboard'))  # Adjust the URL to where you want to redirect

    return render_template('order_items.html', items=items, order_id=order_id)


@bp.route('/order_items/update/<int:order_id>/<int:product_id>', methods=['POST'])
def update_order_item(order_id, product_id):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    # Fetch updated values from the form (or json, depending on your setup)
    fulfilled_status = request.form.get('fulfilled_status')  # This should be a boolean or 0/1 value
    fulfillment_date = request.form.get('fulfillment_date')  # Optional, might not be provided

    # Attempt to update the fulfillment status
    if OrderItem.update_fulfillment(order_id, product_id, fulfilled_status, fulfillment_date):
        flash('Order item updated successfully.')
        return redirect(url_for('order_items.get_order_items', order_id=order_id))

    flash('Failed to update order item.')
    return redirect(url_for('order_items.get_order_items', order_id=order_id))


