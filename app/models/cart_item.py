from flask import current_app as app
from sqlalchemy import text
import traceback

class CartItem:
    def __init__(self, user_id, product_id, quantity, saved_for_later, price, product_name):
        self.user_id = user_id
        self.product_id = product_id
        self.quantity = quantity
        self.saved_for_later = saved_for_later
        self.price = price
        self.product_name = product_name

    @staticmethod
    def add_item(user_id, product_id, quantity=1):
        try:
            with app.db.engine.begin() as conn:
                # First, check if the product exists in the inventory
                inventory_check = conn.execute(text('''
                    SELECT quantity 
                    FROM Inventory 
                    WHERE product_id = :product_id
                '''), {"product_id": product_id}).fetchone()

                # If no inventory exists, return a specific flag
                if not inventory_check:
                    return "out_of_stock"

                available_inventory = inventory_check[0]

                # Check existing cart items for this product
                existing_cart_item = conn.execute(text('''
                    SELECT quantity 
                    FROM Cart_Items 
                    WHERE user_id = :user_id AND product_id = :product_id
                '''), {"user_id": user_id, "product_id": product_id}).fetchone()

                # Calculate potential new quantity in cart
                current_cart_quantity = existing_cart_item[0] if existing_cart_item else 0
                total_requested_quantity = current_cart_quantity + quantity

                # Check if requested quantity exceeds available inventory
                if total_requested_quantity > available_inventory:
                    return "out_of_stock"

                # If checks pass, add or update cart item
                conn.execute(text('''
                INSERT INTO Cart_Items (user_id, product_id, quantity)
                VALUES (:user_id, :product_id, :quantity)
                ON CONFLICT (user_id, product_id) DO UPDATE
                SET quantity = Cart_Items.quantity + :quantity
                '''), {"user_id": user_id, "product_id": product_id, "quantity": quantity})
                
                return True

        except Exception as e:
            print(f"Error adding product {product_id} to cart for user {user_id}: {str(e)}")
            print(traceback.format_exc())
            return False

    @staticmethod
    def update_quantity(user_id, product_id, quantity):
        try:
            with app.db.engine.begin() as conn:
                conn.execute(text('''
                UPDATE Cart_Items
                SET quantity = :quantity
                WHERE user_id = :user_id AND product_id = :product_id
                '''),
                {"user_id": user_id, "product_id": product_id, "quantity": quantity})
                print(f"Updated quantity for product {product_id} in user {user_id}'s cart")
                return True
        except Exception as e:
            print(f"Error updating quantity: {str(e)}")
            print(traceback.format_exc())
            return False

    @staticmethod
    def delete(user_id, product_id):
        try:
            with app.db.engine.begin() as conn:
                conn.execute(text('''
                DELETE FROM Cart_Items
                WHERE user_id = :user_id AND product_id = :product_id
                '''),
                {"user_id": user_id, "product_id": product_id})
                print(f"Deleted product {product_id} from user {user_id}'s cart")
                return True
        except Exception as e:
            print(f"Error deleting cart item: {str(e)}")
            print(traceback.format_exc())
            return False

    @staticmethod
    def save_for_later(user_id, product_id):
        try:
            with app.db.engine.begin() as conn:
                conn.execute(text('''
                UPDATE Cart_Items
                SET saved_for_later = TRUE
                WHERE user_id = :user_id AND product_id = :product_id
                '''),
                {"user_id": user_id, "product_id": product_id})
                print(f"Saved product {product_id} for later in user {user_id}'s cart")
                return True
        except Exception as e:
            print(f"Error saving item for later: {str(e)}")
            print(traceback.format_exc())
            return False

    @staticmethod
    def restore_to_cart(user_id, product_id):
        try:
            with app.db.engine.begin() as conn:
                conn.execute(text('''
                UPDATE Cart_Items
                SET saved_for_later = FALSE
                WHERE user_id = :user_id AND product_id = :product_id
                '''),
                {"user_id": user_id, "product_id": product_id})
                print(f"Restored product {product_id} to user {user_id}'s cart")
                return True
        except Exception as e:
            print(f"Error restoring item to cart: {str(e)}")
            print(traceback.format_exc())
            return False

    @staticmethod
    def get_all_by_user(user_id):
        try:
            # Execute the query and get results as a list of tuples
            rows = app.db.execute('''
            SELECT c.user_id, c.product_id, c.quantity, c.saved_for_later, p.price, p.name
            FROM Cart_Items c
            JOIN Products p ON c.product_id = p.id
            WHERE c.user_id = :user_id
            ''', {"user_id": user_id})

            # Include product name (row[5]) when creating CartItem instances
            return [CartItem(row[0], row[1], row[2], row[3], row[4], row[5]) for row in rows]
        except Exception as e:
            print(f"Error fetching cart items: {str(e)}")
            print(traceback.format_exc())
            return []

    @staticmethod
    def get_cart_count(user_id):
        try:
            # Execute a query to sum the quantity of items in the cart for the user
            result = app.db.execute('''
            SELECT COALESCE(SUM(quantity), 0)
            FROM Cart_Items
            WHERE user_id = :user_id AND saved_for_later = FALSE
            ''', {"user_id": user_id})

            # Extract the count from the result
            return result[0][0] if result else 0
        except Exception as e:
            print(f"Error fetching cart item count: {str(e)}")
            print(traceback.format_exc())
            return 0
