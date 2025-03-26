from flask import current_app as app
from flask_login import current_user, login_required

class OrderedItemsInfo:
    def __init__(self, id, date_order_placed, fulfilled, buyer_id, seller_id, product_id, total_items, buyer_address):
        self.id = id
        self.date_order_placed = date_order_placed
        self.fulfilled = fulfilled
        self.buyer_id = buyer_id
        self.seller_id = seller_id
        self.product_id = product_id
        self.total_items = total_items
        self.buyer_address = buyer_address
    
    @staticmethod
    def get_fulfilled_orders_by_seller_id(seller_id):
        """Retrieve fulfilled orders for products sold by the specific seller."""
        result = app.db.execute(
            """
            SELECT 
                oi.id, 
                oi.date_order_placed, 
                oi.fulfilled, 
                oi.buyer_id, 
                oi.seller_id, 
                oi.product_id, 
                oi.total_items, 
                oi.buyer_address 
            FROM Ordered_Items_Info oi
            JOIN Products p ON oi.product_id = p.id
            WHERE oi.seller_id = :seller_id AND oi.fulfilled = TRUE 
            AND oi.buyer_id != :seller_id
            ORDER BY oi.date_order_placed DESC
            """,
            {"seller_id": seller_id}
        )
        return [OrderedItemsInfo(*row) for row in result]

    @staticmethod
    def get_not_fulfilled_orders_by_seller_id(seller_id):
        """Retrieve not fulfilled orders for products sold by the specific seller."""
        result = app.db.execute(
            """
            SELECT 
                oi.id, 
                oi.date_order_placed, 
                oi.fulfilled, 
                oi.buyer_id, 
                oi.seller_id, 
                oi.product_id, 
                oi.total_items, 
                oi.buyer_address 
            FROM Ordered_Items_Info oi
            JOIN Products p ON oi.product_id = p.id
            WHERE oi.seller_id = :seller_id AND oi.fulfilled = FALSE 
            AND oi.buyer_id != :seller_id
            ORDER BY oi.date_order_placed DESC
            """,
            {"seller_id": seller_id}
        )
        return [OrderedItemsInfo(*row) for row in result]
        
    @staticmethod
    def update_fulfillment_status(order_id, status):
        try:
            # First, get the details of the specific order item
            order_item = app.db.execute(
                """
                SELECT order_id, product_id 
                FROM Ordered_Items_Info 
                WHERE id = :order_id
                """, 
                {"order_id": order_id}
            )

            if not order_item:
                print(f"No order item found for order_id: {order_id}")
                return False

            # Unpack the order_id and product_id
            order_buy_id, product_id = order_item[0]

            # Update Ordered_Items_Info
            app.db.execute('''
                UPDATE Ordered_Items_Info
                SET fulfilled = :status
                WHERE id = :order_id
            ''', {
                "status": status,
                "order_id": order_id
            })

            # Update Order_Items
            app.db.execute('''
                UPDATE Order_Items
                SET fulfilled = :status,
                    fulfillment_date = CASE WHEN :status = TRUE THEN CURRENT_TIMESTAMP ELSE NULL END
                WHERE order_id = :order_buy_id AND product_id = :product_id
            ''', {
                "status": status,
                "order_buy_id": order_buy_id,
                "product_id": product_id
            })

            return True
        except Exception as e:
            print(f"Error updating fulfillment status: {e}")
            return False
        
    @staticmethod
    def get_order_by_id(order_id):
        """Retrieve a specific order by its order ID."""
        result = app.db.execute(
            """
            SELECT id, date_order_placed, fulfilled, buyer_id, seller_id, product_id, total_items, buyer_address
            FROM Ordered_Items_Info
            WHERE id = :order_id
            """,
            order_id=order_id
        )
        
        # Fetch the first result (if there is any result)
        row = result[0] if result else None

        # If a row is found, create and return the OrderedItemsInfo object, else return None
        if row:
            return OrderedItemsInfo(*row)
        else:
            return None
