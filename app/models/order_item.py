from flask import current_app as app
from sqlalchemy import text
import traceback

class OrderItem:
    def __init__(self, order_id, product_id, quantity, unit_price, fulfilled=False, fulfillment_date=None, product_name=None):
        self.order_id = order_id
        self.product_id = product_id
        self.quantity = quantity
        self.unit_price = unit_price
        self.fulfilled = fulfilled
        self.fulfillment_date = fulfillment_date
        self.product_name = product_name  # Add product_name

    @staticmethod
    def get_by_order_id(order_id):
        try:
            rows = app.db.execute('''
            SELECT oi.order_id, oi.product_id, oi.quantity, oi.unit_price, oi.fulfilled, oi.fulfillment_date, p.name AS product_name
            FROM Order_Items oi
            JOIN Products p ON oi.product_id = p.id
            WHERE oi.order_id = :order_id
            ''', {"order_id": order_id})

            # Manually map the result rows using tuple indexing
            return [
                OrderItem(
                    order_id=row[0],
                    product_id=row[1],
                    quantity=row[2],
                    unit_price=row[3],
                    fulfilled=row[4],
                    fulfillment_date=row[5],
                    product_name=row[6]
                ) for row in rows
            ]
        except Exception as e:
            print(f"Error fetching order items for order {order_id}: {str(e)}")
            print(traceback.format_exc())
            return []

    @staticmethod
    def update_fulfillment(order_id, product_id, fulfilled, fulfillment_date=None):
        try:
            with app.db.engine.begin() as conn:
                conn.execute(text('''
                UPDATE Order_Items
                SET fulfilled = :fulfilled, fulfillment_date = :fulfillment_date
                WHERE order_id = :order_id AND product_id = :product_id
                '''), {
                    "order_id": order_id,
                    "product_id": product_id,
                    "fulfilled": fulfilled,
                    "fulfillment_date": fulfillment_date
                })
            print(f"Fulfillment status updated for order {order_id}, product {product_id}")
            return True
        except Exception as e:
            print(f"Error updating fulfillment for order {order_id}, product {product_id}: {str(e)}")
            print(traceback.format_exc())
            return False

    @staticmethod
    def delete(order_id, product_id):
        try:
            with app.db.engine.begin() as conn:
                conn.execute(text('''
                DELETE FROM Order_Items
                WHERE order_id = :order_id AND product_id = :product_id
                '''), {"order_id": order_id, "product_id": product_id})
            print(f"Order item for order {order_id}, product {product_id} deleted successfully")
            return True
        except Exception as e:
            print(f"Error deleting order item for order {order_id}, product {product_id}: {str(e)}")
            print(traceback.format_exc())
            return False
