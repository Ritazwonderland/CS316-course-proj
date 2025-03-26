from flask import current_app as app
from .product import Product
from .user import User
from flask_login import current_user, login_required
from sqlalchemy import text
from .ordered_Items_Info import OrderedItemsInfo


class Inventory:
    def __init__(self, user_id, product_id, quantity):
        self.user_id = user_id
        self.product_id = product_id
        self.quantity = quantity

    @staticmethod
    def get_all_by_user_id(user_id):

        if not isinstance(user_id, int) or user_id < 0:
            print("Invalid user_id provided.")
            return []  # Return an empty list for invalid user_id

        result = app.db.execute(
            """
                SELECT 
                    i.product_id,
                    p.name,
                    i.quantity,
                    SUM(oi.total_items) AS popularity  -- Sum of total_items from orders for each product
                FROM Inventory i
                JOIN Products p ON i.product_id = p.id
                LEFT JOIN ordered_items_info oi ON oi.product_id = i.product_id  -- Join with ordered_items_info
                WHERE i.user_id = :user_id
                GROUP BY i.product_id, p.name, i.quantity  -- Group by product to calculate the sum
            """,
            {"user_id": user_id}  # Passing the user_id as a named parameter
        ) 
        return result

    @staticmethod
    def add_product(user_id, product_id, quantity):
        """Add a product to the user's inventory or update if it already exists."""

        # Fetch current quantity if product exists in inventory
        existing_product = app.db.execute(
            """
            SELECT quantity FROM Inventory
            WHERE user_id = :user_id AND product_id = :product_id
            """,
            {"user_id": user_id, "product_id": product_id}
        )

        try:
            with app.db.engine.begin() as conn:
                if existing_product:
                    # If product exists, update the quantity
                    current_quantity = existing_product[0][0]  # Access the first item in the row
                    new_quantity = current_quantity + quantity
                    conn.execute(
                        text("""
                        UPDATE Inventory
                        SET quantity = :new_quantity
                        WHERE user_id = :user_id AND product_id = :product_id
                        """),
                        {"new_quantity": new_quantity, "user_id": user_id, "product_id": product_id}
                    )
                else:
                    # Insert a new product if it doesn't exist
                    conn.execute(
                        text("""
                        INSERT INTO Inventory (user_id, product_id, quantity)
                        VALUES (:user_id, :product_id, :quantity)
                        """),
                        {"user_id": user_id, "product_id": product_id, "quantity": quantity}
                    )
            print(f"Product {product_id} updated or added to user {user_id}'s inventory with quantity {quantity}.")
            return True
        except Exception as e:
            print(f"Error adding product {product_id} to inventory for user {user_id}: {e}")
            return False

    @staticmethod
    def remove_product(user_id, product_id, quantity):
        """Remove a specified quantity of a product from the user's inventory."""
        try:
            # Fetch the current quantity of the product in the user's inventory
            result = app.db.execute("""
                SELECT quantity
                FROM Inventory
                WHERE user_id = :user_id AND product_id = :product_id
            """, {"user_id": user_id, "product_id": product_id})

            # If no such product exists in the user's inventory
            if not result:
                print(f"Product {product_id} not found in inventory for user {user_id}")
                return False

            current_quantity = result[0][0]

            # Check if the current quantity is greater than or equal to the quantity to be removed
            if current_quantity >= quantity:
                new_quantity = current_quantity - quantity
                # Update the quantity of the product in the inventory
                with app.db.engine.begin() as conn:
                    conn.execute(text("""
                        UPDATE Inventory
                        SET quantity = :new_quantity
                        WHERE user_id = :user_id AND product_id = :product_id
                    """), {"new_quantity": new_quantity, "user_id": user_id, "product_id": product_id})
                print(f"Removed {quantity} of product {product_id} from inventory for user {user_id}")
                return True
            else:
                # If trying to remove more than available, remove the product entirely
                with app.db.engine.begin() as conn:
                    conn.execute(text("""
                        DELETE FROM Inventory
                        WHERE user_id = :user_id AND product_id = :product_id
                    """), {"user_id": user_id, "product_id": product_id})
                print(f"Removed product {product_id} from inventory for user {user_id} (not enough quantity)")
                return True
        
        except Exception as e:
            print(f"Error removing product {product_id} from inventory: {str(e)}")
            return False
