from flask import Blueprint, flash, redirect, url_for, render_template, request
from flask_login import login_required, current_user
from app.models.cart_item import CartItem
from app.models.order_buy import OrderBuy
import traceback

bp = Blueprint('cart_items', __name__)

@bp.route('/cart', methods=['GET'])
@login_required
def get_cart():
    # Fetch all cart items for the current user
    all_items = CartItem.get_all_by_user(current_user.id)
    
    # Separate cart items from saved-for-later items
    cart_items = [item for item in all_items if not item.saved_for_later]
    saved_items = [item for item in all_items if item.saved_for_later]
    
    # Calculate the total price of the cart items
    total = sum(item.price * item.quantity for item in cart_items)
    
    return render_template('cart.html', cart_items=cart_items, saved_items=saved_items, total=total)

@bp.route('/add_to_cart/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    try:
        result = CartItem.add_item(current_user.id, product_id, quantity=1)
        
        if result is True:
            flash('Item added to cart successfully!', 'success')
        elif result == "out_of_stock":
            flash('Sorry, this item is currently out of stock.', 'warning')
        else:
            flash('Failed to add item to cart.', 'error')
    except Exception as e:
        print(f"Error in add_to_cart: {str(e)}")
        print(traceback.format_exc())
        flash('An error occurred while adding the item to the cart.', 'error')
    return redirect(url_for('index.index'))

@bp.route('/cart/update/<int:item_id>', methods=['POST'])
@login_required
def update_cart_item(item_id):
    # Get the new quantity from the form
    new_quantity = request.form.get('quantity', type=int)
    
    # Update the cart item quantity
    if new_quantity and new_quantity > 0:
        CartItem.update_quantity(current_user.id, item_id, new_quantity)
        flash('Quantity updated.', 'success')
    else:
        flash('Invalid quantity provided.', 'danger')

    return redirect(url_for('cart_items.get_cart'))

@bp.route('/cart/remove/<int:item_id>', methods=['POST'])
@login_required
def remove_from_cart(item_id):
    # Remove the item from the cart
    CartItem.delete(current_user.id, item_id)
    flash('Item removed from cart.', 'success')
    return redirect(url_for('cart_items.get_cart'))

@bp.route('/cart/save/<int:item_id>', methods=['POST'])
@login_required
def save_for_later(item_id):
    # Move the item to "saved for later"
    CartItem.save_for_later(current_user.id, item_id)
    flash('Item saved for later.', 'success')
    return redirect(url_for('cart_items.get_cart'))

@bp.route('/cart/restore/<int:item_id>', methods=['POST'])
@login_required
def restore_to_cart(item_id):
    # Restore the item from "saved for later" to the cart
    CartItem.restore_to_cart(current_user.id, item_id)
    flash('Item restored to cart.', 'success')
    return redirect(url_for('cart_items.get_cart'))

@bp.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    # Fetch all cart items for the current user
    cart_items = CartItem.get_all_by_user(current_user.id)
    cart_items = [item for item in cart_items if not item.saved_for_later]

    # Calculate total price
    total = sum(item.price * item.quantity for item in cart_items)

    # If POST request, handle checkout submission
    if request.method == 'POST':
        # Use the OrderBuy.add method to process the order
        order_result = OrderBuy.add(current_user.id)
        
        # Check if order was successfully placed
        if isinstance(order_result, dict) and order_result.get('order_placed'):
            # Extract the order ID from the returned OrderBuy object
            order_id = order_result['order'].order_id
            
            flash(f"Order #{order_id} placed successfully!", 'success')
            return redirect(url_for('order_items.get_order_items', order_id=order_id))
        
        # Check for insufficient inventory
        if isinstance(order_result, dict):
            # Flash messages for insufficient inventory
            if 'insufficient_items' in order_result:
                for item in order_result['insufficient_items']:
                    flash(
                        f"Insufficient inventory for {item['product_name']}: "
                        f"Only {item['inventory_quantity']} available, "
                        f"but {item['cart_quantity']} requested.", 'danger'
                    )
            
            # Check for insufficient funds
            if 'error' in order_result:
                flash(order_result['error'], 'danger')
            
            # Render the checkout page again with flashed messages
            addresses = current_user.get_addresses()
            return render_template(
                'checkout.html',
                cart_items=cart_items,
                total=total,
                addresses=addresses
            )

    # Get user's addresses for shipping selection
    addresses = current_user.get_addresses()

    return render_template('checkout.html', cart_items=cart_items, total=total, addresses=addresses)