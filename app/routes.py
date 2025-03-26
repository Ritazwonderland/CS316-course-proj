from flask import Flask, render_template, redirect, url_for, Blueprint, flash, request, jsonify, make_response
from flask_login import current_user, login_required, logout_user, login_user
from flask import current_app, session
from app.models.user import User
from app.models.address import Address
from app.forms import LoginForm, RegistrationForm, UserPurchasesForm, EditProfileForm, AddAddressForm, ChangePasswordForm, TopUpForm, WithdrawForm  # Add TopUpForm and WithdrawForm here
import traceback
from werkzeug.urls import url_parse
from app.models.wish import Wish
from app import db
from sqlalchemy import text  # Add this import
from datetime import datetime, timedelta
from app.models.cart_item import CartItem
from app.models.order_buy import OrderBuy

app = Flask(__name__)

# Assuming you have a blueprint for user-related routes
bp = Blueprint('users', __name__)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.register(form.email.data,
                        form.password.data,
                        form.firstname.data,
                        form.lastname.data):
            flash('Congratulations', 'success')
            return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = User.get_by_auth(form.email.data.strip().lower(), form.password.data)
            if user:
                login_user(user, remember=form.remember_me.data)
                next_page = request.args.get('next')
                if not next_page or url_parse(next_page).netloc != '':
                    next_page = url_for('index.index')
                return redirect(next_page)
        except Exception as e:
            flash('An error occurred during login. Please try again.', 'danger')
            return redirect(url_for('users.login'))
    
    return render_template('login.html', title='Sign In', form=form)

@bp.route('/logout')
def logout():
    if current_user.is_authenticated:
        # Store a flag in session to indicate recent logout
        session['just_logged_out'] = True
        logout_user()
        flash('You have been successfully logged out.', 'info')
        # Create response with cache control headers
        response = make_response(redirect(url_for('index.index')))
        # Set cache control headers to prevent caching
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, private'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        # Clear any session data except the logout flag
        session.clear()
        session['just_logged_out'] = True
        return response
    return redirect(url_for('index.index'))

@bp.before_request
def check_authentication():
    """Check if user is trying to access authenticated pages after logout"""
    if not current_user.is_authenticated:
        # List of protected endpoints that require authentication
        protected_endpoints = [
            'users.profile',
            'users.edit_profile',
            'order_history.order_history',
            'cart_items.get_cart',
            'users.change_password',
            'users.add_address',
            'users.withdraw',
            'users.top_up',
            'inventory.inventory'
        ]
        
        if request.endpoint in protected_endpoints:
            # Store the attempted URL for redirecting after login
            session['next'] = request.url
            flash('Please log in to access this page.', 'info')
            return redirect(url_for('index.index'))

@bp.route('/wishlist')
@login_required
def wishlist():
    items = Wish.get_all_by_user_id(current_user.id)
    return render_template('wishlist.html', wishlist=items)

@bp.route('/add_to_wishlist/<int:product_id>', methods=['POST'])
@login_required
def add_to_wishlist(product_id):
    try:
        if Wish.add_wish(current_user.id, product_id):
            flash('Item added to wishlist successfully!', 'success')
        else:
            flash('Failed to add item to wishlist. It might already be in your wishlist.', 'warning')
    except Exception as e:
        print(f"Error in add_to_wishlist: {str(e)}")
        print(traceback.format_exc())
        flash('An error occurred while adding the item to the wishlist.', 'error')
    return redirect(url_for('index.index'))

@bp.route('/remove_from_wishlist/<int:product_id>', methods=['POST'])
@login_required
def remove_from_wishlist(product_id):
    if Wish.remove_wish(current_user.id, product_id):
        flash('Item removed from wishlist successfully!', 'success')
    else:
        flash('Failed to remove item from wishlist.', 'error')
    return redirect(url_for('users.wishlist'))

@bp.route('/profile')
@login_required
def profile():
    # Get user's addresses
    addresses = current_app.db.execute('''
        SELECT id, street, city, state, zip_code, is_default
        FROM Addresses
        WHERE user_id = :user_id
        ORDER BY is_default DESC, id ASC
    ''', {'user_id': current_user.id})

    # Get user's order history using the new method
    orders = OrderBuy.get_all_by_user(current_user.id)
    
    # Calculate total spent
    total_spent = OrderBuy.get_total_spent(current_user.id)
    
    # Get cart items count
    cart_items_count = CartItem.get_cart_count(current_user.id)
    
    # Get total orders and recent orders
    total_orders = OrderBuy.get_total_orders(current_user.id)
    
    # Get recent orders (last 30 days)
    recent_orders = len([order for order in orders 
                        if order.order_date >= datetime.now() - timedelta(days=30)]) if orders else 0
    
    # Get recent activities
    recent_activities = []
    for order in orders[:10]:
        recent_activities.append({
            'timestamp': order.order_date,
            'action': 'Order',
            'details': f'Order ID: {order.order_id}',
            'amount': order.total_price
        })

    # Get user's balance
    balance = current_user.get_balance() if hasattr(current_user, 'get_balance') else 0.0

    return render_template('profile.html',
                         title='User Profile',
                         user=current_user,
                         addresses=addresses,
                         balance=balance,
                         total_spent=total_spent,
                         cart_items=cart_items_count,
                         total_orders=total_orders,
                         recent_orders=recent_orders,
                         recent_activities=recent_activities,
                         orders=orders)  # Added orders to context for potential use in template

@bp.route('/order/<int:order_id>')
@login_required
def order_details(order_id):
    order = Order.get(order_id)
    if order and order.user_id == current_user.id:
        return render_template('order_details.html', order=order)
    flash('Order not found or you do not have permission to view it.', 'error')
    return redirect(url_for('users.profile', _anchor='v-pills-dashboard'))

@bp.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    if current_user.id != 7:  # Only allow access to admin (uid == 7)
        flash('You do not have permission to access this page.', 'error')
        return redirect(url_for('index.index'))

    form = UserPurchasesForm()
    user_orders = None
    user = None
    searched = False

    if form.validate_on_submit():
        user_id = form.user_id.data
        searched = True
        user = User.get(user_id)
        if user:
            # Use OrderBuy method to get user's orders
            user_orders = OrderBuy.get_all_by_user(user_id)
            
            if not user_orders:
                flash(f'No order history found for user with ID {user_id}.', 'info')
            else:
                # Optional: Calculate summary if needed
                total_orders = len(user_orders)
                total_spent = sum(order.total_price for order in user_orders)
                # You can pass these as additional context if desired
        else:
            flash(f'No user found with ID {user_id}.', 'warning')
    else:
        if request.method == 'POST':
            flash('Invalid input. Please enter a non-negative integer for User ID.', 'error')

    return render_template('admin.html', 
                           form=form, 
                           user_orders=user_orders, 
                           user=user, 
                           searched=searched)

@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        try:
            with current_app.db.engine.begin() as conn:
                result = conn.execute(text('''
UPDATE Users
SET firstname = :firstname, lastname = :lastname, email = :email
WHERE id = :user_id
'''),
                               {"firstname": form.firstname.data,
                                "lastname": form.lastname.data,
                                "email": form.email.data,
                                "user_id": current_user.id})
                
                if result.rowcount > 0:
                    current_user.firstname = form.firstname.data
                    current_user.lastname = form.lastname.data
                    current_user.email = form.email.data
                    flash('Your profile has been successfully updated!', 'success')
                    return redirect(url_for('users.profile', _anchor='v-pills-profile'))
                else:
                    flash('No changes were made to your profile.', 'info')
        except Exception as e:
            flash(f'An error occurred while updating your profile: {str(e)}', 'danger')
    elif form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'{field.capitalize()}: {error}', 'danger')
    
    form.firstname.data = current_user.firstname
    form.lastname.data = current_user.lastname
    form.email.data = current_user.email
    return render_template('edit_profile.html', title='Edit Profile', form=form)

@bp.route('/add_address', methods=['GET', 'POST'])
@login_required
def add_address():
    form = AddAddressForm()
    if form.validate_on_submit():
        try:
            new_address = Address.add_address(
                current_user.id,
                form.street.data,
                form.city.data,
                form.state.data,
                form.zip_code.data,
                form.is_default.data
            )
            if new_address:
                flash('New address added successfully.')
                return redirect(url_for('users.profile', _anchor='v-pills-addresses'))
            else:
                flash('Failed to add new address. Please try again.', 'error')
        except Exception as e:
            flash('An error occurred while adding the address. Please try again.', 'error')
    return render_template('add_address.html', title='Add Address', form=form)

@bp.route('/edit_address/<int:address_id>', methods=['GET', 'POST'])
@login_required
def edit_address(address_id):
    address = Address.get(address_id)
    if address.user_id != current_user.id:
        flash('You do not have permission to edit this address.', 'error')
        return redirect(url_for('users.profile', _anchor='v-pills-addresses'))
    
    form = AddAddressForm(obj=address)
    if form.validate_on_submit():
        address.street = form.street.data
        address.city = form.city.data
        address.state = form.state.data
        address.zip_code = form.zip_code.data
        address.is_default = form.is_default.data
        if Address.update(address):
            flash('Address updated successfully.', 'success')
            return redirect(url_for('users.profile', _anchor='v-pills-addresses'))
        else:
            flash('Failed to update address.', 'error')
    return render_template('edit_address.html', form=form, address=address)

@bp.route('/set_default_address/<int:address_id>', methods=['POST'])
@login_required
def set_default_address(address_id):
    if Address.set_default(address_id, current_user.id):
        flash('Default address updated successfully.', 'success')
    else:
        flash('Failed to update default address.', 'error')
    return redirect(url_for('users.profile', _anchor='v-pills-addresses'))

@bp.route('/delete_address/<int:address_id>', methods=['POST'])
@login_required
def delete_address(address_id):
    address = Address.get(address_id)
    if not address:
        flash('Address not found.', 'error')
    elif address.user_id != current_user.id:
        flash('You do not have permission to delete this address.', 'error')
    elif address.is_default:
        flash('You cannot delete the default address.', 'error')
    elif Address.delete(address_id):
        flash('Address deleted successfully.', 'success')
    else:
        flash('Failed to delete address.', 'error')
    return redirect(url_for('users.profile', _anchor='v-pills-addresses'))

@bp.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.check_password(form.current_password.data):
            try:
                current_user.set_password(form.new_password.data)
                flash('Your password has been successfully updated!', 'success')
                return redirect(url_for('users.profile', _anchor='v-pills-security'))
            except Exception as e:
                flash(f'An error occurred while updating your password. Please try again.', 'danger')
        else:
            flash('The current password you entered is incorrect. Please try again.', 'danger')
    return render_template('change_password.html', form=form)

@bp.route('/top_up', methods=['GET', 'POST'])
@login_required
def top_up():
    form = TopUpForm()
    if form.validate_on_submit():
        amount = form.amount.data
        print(f"Attempting to top up ${amount:.2f} to user {current_user.id}'s account")
        transaction_id = current_user.add_funds(amount)
        if transaction_id:
            print(f"Successfully topped up ${amount:.2f} to user {current_user.id}'s account. Transaction ID: {transaction_id}")
            new_balance = current_user.get_balance()
            print(f"New balance for user {current_user.id}: ${new_balance:.2f}")
            flash(f'Successfully topped up ${amount:.2f} to your account. New balance: ${new_balance:.2f}', 'success')
            return redirect(url_for('users.profile', _anchor='v-pills-balance'))
        else:
            print(f"Failed to top up ${amount:.2f} to user {current_user.id}'s account")
            flash('Failed to top up. Please try again.', 'danger')
    return render_template('top_up.html', form=form)

@bp.route('/withdraw', methods=['GET', 'POST'])
@login_required
def withdraw():
    form = WithdrawForm()
    current_balance = current_user.get_balance()
    if form.validate_on_submit():
        amount = form.amount.data
        if amount > current_balance:
            flash(f'Insufficient funds. Your current balance is ${current_balance:.2f}', 'danger')
        else:
            transaction_id = current_user.withdraw_funds(amount)
            if transaction_id:
                new_balance = current_user.get_balance()
                flash(f'Successfully withdrew ${amount:.2f} from your account. New balance: ${new_balance:.2f}', 'success')
                return redirect(url_for('users.profile', _anchor='v-pills-balance'))
            else:
                flash('Failed to withdraw funds. Please try again.', 'danger')
    return render_template('withdraw.html', form=form, current_balance=current_balance)

# Add cache control headers only to sensitive routes
@bp.after_request
def add_security_headers(response):
    # List of sensitive endpoints that should not be cached
    sensitive_endpoints = [
        'users.profile',
        'users.edit_profile',
        'order_history.order_history',
        'cart_items.get_cart',
        'users.change_password',
        'users.add_address',
        'users.withdraw',
        'users.top_up'
    ]
    
    # Only add no-cache headers for sensitive routes
    if (current_user.is_authenticated and 
        request.endpoint in sensitive_endpoints):
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
    return response

