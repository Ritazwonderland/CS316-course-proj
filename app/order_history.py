from flask import Blueprint, render_template, request, redirect
from flask_login import current_user, login_required
from .models.ordered_Items_Info import OrderedItemsInfo
import datetime
from humanize import naturaltime

def humanize_time(dt):
    return naturaltime(datetime.datetime.now() - dt)

bp = Blueprint('order_history', __name__)

@bp.route('/order_history')
@login_required
def order_history():
    """Display the history of orders for the current seller."""
    # Retrieve fulfilled and not fulfilled orders specific to the seller
    fulfilled_orders = OrderedItemsInfo.get_fulfilled_orders_by_seller_id(current_user.id)
    not_fulfilled_orders = OrderedItemsInfo.get_not_fulfilled_orders_by_seller_id(current_user.id)

    return render_template('order_history.html',
                           fulfilled_orders=fulfilled_orders,
                           not_fulfilled_orders=not_fulfilled_orders)

@bp.route('/update_fulfillment/<int:order_id>/<int:status>', methods=['POST'])
@login_required
def update_fulfillment(order_id, status):
    """Update fulfillment status of a specific order."""
    # Verify the order belongs to the current seller
    order = OrderedItemsInfo.get_order_by_id(order_id)
    
    if order and order.seller_id == current_user.id:
        # Update the fulfillment status (1 for fulfilled, 0 for not fulfilled)
        OrderedItemsInfo.update_fulfillment_status(order_id, bool(status))
        return redirect('/order_history')
    else:
        return "Unauthorized", 403

@bp.route('/order_info/<int:order_id>')
@login_required
def order_info(order_id):
    """Display detailed information about a specific order."""
    # Retrieve the order details by order_id
    order = OrderedItemsInfo.get_order_by_id(order_id)
    
    if order and order.seller_id == current_user.id:
        return render_template('order_info.html', order=order)
    else:
        return "Order not found or unauthorized", 403
