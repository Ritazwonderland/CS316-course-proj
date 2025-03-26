from flask import render_template, redirect, url_for, request, flash
from flask_login import current_user, login_required
from .models.inventory import Inventory 
from flask import Blueprint
from sqlalchemy import text


bp = Blueprint('inventory', __name__)

@bp.route('/inventory', methods=['GET', 'POST'])
def inventory():
    inventory_items = []  # Initialize as an empty list

    # Fetch inventory for the current user
    if current_user.id != None:
        inventory_items = list(Inventory.get_all_by_user_id(current_user.id))  # Fetch inventory for the specified user_id

    # Handle form submission on POST request
    if request.method == 'POST':
        action = request.form.get('action')
        product_id = request.form.get('product_id')
        quantity = request.form.get('quantity', type=int)

        if action == 'add':
            Inventory.add_product(current_user.id, product_id, quantity)
            flash('Product added to inventory successfully!', 'success')

        elif action == 'remove':
            Inventory.remove_product(current_user.id, product_id, quantity)
            flash('Product removed from inventory successfully!', 'success')

        return redirect(url_for('inventory.inventory'))  # Redirect to the inventory page

    # Render the template with the current inventory items and user_id
    return render_template('inventory.html', inventory_items=inventory_items)
