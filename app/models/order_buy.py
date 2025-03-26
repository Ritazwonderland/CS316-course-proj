from flask import current_app as app
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
import traceback
from datetime import datetime
from .balance import BalanceTransaction

class OrderBuy:
    def __init__(self, order_id, user_id, total_price, order_date, order_status, total_items=0):
        self.order_id = order_id
        self.user_id = user_id
        self.total_price = total_price
        self.order_date = order_date
        self.order_status = order_status
        self.total_items = total_items  # New attribute
        
    @staticmethod
    def add(user_id):
        try:
            print(f"OrderBuy.add() called for user: {user_id}")

            # Fetch cart items for the user with detailed inventory check
            cart_items = app.db.execute('''
                SELECT 
                    c.product_id, 
                    c.quantity AS cart_quantity, 
                    p.price AS unit_price, 
                    p.name AS product_name,
                    COALESCE(i.quantity, 0) AS inventory_quantity,
                    COALESCE((SELECT user_id FROM Inventory WHERE product_id = c.product_id LIMIT 1), :user_id) AS seller_id
                FROM Cart_Items c
                JOIN Products p ON c.product_id = p.id
                LEFT JOIN Inventory i ON c.product_id = i.product_id
                WHERE c.user_id = :user_id AND c.saved_for_later = FALSE
            ''', {"user_id": user_id})

            print(f"Cart items fetched: {cart_items}")

            # Comprehensive inventory check
            insufficient_items = []
            for item in cart_items:
                product_id, cart_quantity, unit_price, product_name, inventory_quantity, seller_id = item
                if cart_quantity > inventory_quantity:
                    insufficient_items.append({
                        'product_id': product_id,
                        'product_name': product_name,
                        'cart_quantity': cart_quantity,
                        'inventory_quantity': inventory_quantity
                    })

            # If any items have insufficient inventory, return details
            if insufficient_items:
                return {
                    'order_placed': False,
                    'insufficient_items': insufficient_items
                }

            if not cart_items:
                print("Cart is empty, cannot place an order.")
                return {
                    'order_placed': False,
                    'insufficient_items': [],
                    'error': 'Cart is empty'
                }

            # Calculate total price from the user's cart
            total_price = sum(item[1] * item[2] for item in cart_items)
            print(f"Total price for order: {total_price}")

            # Check buyer's balance
            buyer_balance = BalanceTransaction.get_balance(user_id)
            if buyer_balance < total_price:
                print("Insufficient balance to complete the order")
                return {
                    'order_placed': False,
                    'insufficient_items': [],
                    'error': 'Insufficient funds. Please add more balance to your account.'
                }

            with app.db.engine.begin() as conn:
                # Insert new order
                print("Inserting new order into Orders_Buy table...")
                result = conn.execute(text('''
                    INSERT INTO Orders_Buy(user_id, total_price)
                    VALUES(:user_id, :total_price)
                    RETURNING order_id
                '''), {"user_id": user_id, "total_price": total_price})

                rows = result.fetchall()
                if not rows:
                    print("Failed to insert order")
                    return {
                        'order_placed': False,
                        'insufficient_items': [],
                        'error': 'Failed to place order. Please try again later.'
                    }

                order_id = rows[0][0]
                print(f"Order inserted with ID: {order_id}")

                # Deduct total price from buyer's balance
                BalanceTransaction.add_transaction(
                    user_id, 
                    total_price, 
                    'deduct'
                )

                # Track seller balances and update inventory
                seller_earnings = {}

                # Move cart items to Order_Items and Ordered_Items_Info, and update inventory
                for item in cart_items:
                    product_id, quantity, unit_price, product_name, _, seller_id = item
                    item_total = quantity * unit_price
                    print(f"Processing cart item {product_id}...")

                    # Insert into Order_Items
                    conn.execute(text('''
                        INSERT INTO Order_Items(order_id, product_id, quantity, unit_price)
                        VALUES(:order_id, :product_id, :quantity, :unit_price)
                    '''), {
                        "order_id": order_id,
                        "product_id": product_id,
                        "quantity": quantity,
                        "unit_price": unit_price
                    })

                    # Insert into Ordered_Items_Info
                    conn.execute(text('''
                        INSERT INTO Ordered_Items_Info(
                            date_order_placed, fulfilled, buyer_id, seller_id, product_id, 
                            total_items, buyer_address
                        )
                        VALUES(
                            NOW(), FALSE, :buyer_id, :seller_id, :product_id, 
                            :total_items, 
                            (SELECT street || ', ' || city || ', ' || state || ' ' || zip_code 
                            FROM Addresses WHERE user_id = :buyer_id AND is_default = TRUE)
                        )
                    '''), {
                        "buyer_id": user_id,
                        "seller_id": seller_id,
                        "product_id": product_id,
                        "total_items": quantity
                    })

                    # Update Inventory - Reduce the quantity
                    conn.execute(text('''
                        UPDATE Inventory
                        SET quantity = quantity - :order_quantity
                        WHERE user_id = :seller_id AND product_id = :product_id
                    '''), {
                        "order_quantity": quantity,
                        "seller_id": seller_id,
                        "product_id": product_id
                    })

                    # Track earnings for each seller
                    if seller_id not in seller_earnings:
                        seller_earnings[seller_id] = 0
                    seller_earnings[seller_id] += item_total

                # Add balance transactions for sellers
                for seller_id, earnings in seller_earnings.items():
                    BalanceTransaction.add_transaction(
                        seller_id, 
                        earnings, 
                        'add'
                    )

                print("Cart items moved to Order_Items and Ordered_Items_Info tables.")

                # Clear the cart after placing the order
                print("Clearing the cart...")
                conn.execute(text('''
                    DELETE FROM Cart_Items
                    WHERE user_id = :user_id AND saved_for_later = FALSE
                '''), {"user_id": user_id})
                print(f"Cart cleared for user {user_id}")

            return {
                'order_placed': True,
                'insufficient_items': [],  # Ensure empty list is returned if no issues
                'order': OrderBuy(order_id, user_id, total_price, datetime.now(), False)
            }

        except Exception as e:
            print(f"Error adding order: {str(e)}")
            print(traceback.format_exc())
            return {
                'order_placed': False,
                'insufficient_items': [],
                'error': 'An unexpected error occurred. Please try again later.'
            }


    @staticmethod
    def get_all_by_user(user_id):
        try:
            # Pass raw SQL string to app.db.execute, do NOT wrap it with `text()`
            rows = app.db.execute('''
            SELECT 
                ob.order_id, 
                ob.user_id, 
                ob.total_price, 
                ob.order_date, 
                ob.order_status,
                COALESCE(item_count.total_items, 0) as total_items
            FROM Orders_Buy ob
            LEFT JOIN (
                SELECT order_id, SUM(quantity) as total_items
                FROM Order_Items
                GROUP BY order_id
            ) item_count ON ob.order_id = item_count.order_id
            WHERE ob.user_id = :user_id
            ORDER BY ob.order_date DESC
            ''', {"user_id": user_id})

            # Modify the OrderBuy constructor to accept the total_items
            return [OrderBuy(
                order_id=row[0], 
                user_id=row[1], 
                total_price=row[2], 
                order_date=row[3], 
                order_status=row[4],
                total_items=row[5]  # Add this to the OrderBuy constructor
            ) for row in rows]
        except Exception as e:
            print(f"Error fetching orders for user {user_id}: {str(e)}")
            print(traceback.format_exc())
            return []

    @staticmethod
    def delete(order_id):
        try:
            with app.db.engine.begin() as conn:
                # First, delete the associated entries from Ordered_Items_Info
                conn.execute(text('''
                    DELETE FROM Ordered_Items_Info
                    WHERE order_id = :order_id
                '''), {"order_id": order_id})

                # Then, delete the order itself from Orders_Buy
                conn.execute(text('''
                    DELETE FROM Orders_Buy
                    WHERE order_id = :order_id
                '''), {"order_id": order_id})

            print(f"Order {order_id} and its associated items deleted successfully")
            return True
        except SQLAlchemyError as e:
            print(f"Error deleting order {order_id}: {str(e)}")
            print(traceback.format_exc())
            return False


    @staticmethod
    def get_total_orders(user_id):
        try:
            # Count the total number of orders for the user
            result = app.db.execute('''
            SELECT COUNT(*)
            FROM Orders_Buy
            WHERE user_id = :user_id
            ''', {"user_id": user_id})
            
            # Return the total order count
            return result[0][0] if result else 0
        except Exception as e:
            print(f"Error fetching total orders count: {str(e)}")
            print(traceback.format_exc())
            return 0

    @staticmethod
    def get_total_spent(user_id):
        try:
            # Count the total spent
            result = app.db.execute('''
            SELECT COALESCE(SUM(total_price), 0)
            FROM Orders_Buy
            WHERE user_id = :user_id
            ''', {"user_id": user_id})
            
            # Return the total order count
            return result[0][0] if result else 0
        except Exception as e:
            print(f"Error fetching total order cost: {str(e)}")
            print(traceback.format_exc())
            return 0

    @staticmethod
    def get_orders_since(user_id, since_date):
        try:
            rows = app.db.execute('''
            SELECT order_id, user_id, total_price, order_date, order_status
            FROM Orders_Buy
            WHERE user_id = :user_id AND order_date >= :since_date
            ORDER BY order_date DESC
            ''', {"user_id": user_id, "since_date": since_date})

            return [OrderBuy(*row) for row in rows]
        except Exception as e:
            print(f"Error fetching orders for user {user_id} since {since_date}: {str(e)}")
            return []