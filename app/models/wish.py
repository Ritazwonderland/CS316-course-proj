from flask import current_app as app
from sqlalchemy.exc import IntegrityError
from sqlalchemy import text
import traceback

class Wish:
    def __init__(self, id, user_id, product_id, product_name, price):
        self.id = id
        self.user_id = user_id
        self.product_id = product_id
        self.product_name = product_name
        self.price = price

    @staticmethod
    def get_all_by_user_id(user_id):
        rows = app.db.execute('''
SELECT w.id, w.user_id, w.product_id, p.name, p.price
FROM Wishes w
JOIN Products p ON w.product_id = p.id
WHERE w.user_id = :user_id
''',
                              {"user_id": user_id})
        return [Wish(*row) for row in rows]

    @staticmethod
    def get_user_wishlist(user_id):
        return Wish.get_all_by_user_id(user_id)

    @staticmethod
    def add_wish(user_id, product_id):
        try:
            with app.db.engine.begin() as conn:
                result = conn.execute(text('''
INSERT INTO Wishes(user_id, product_id)
VALUES(:user_id, :product_id)
RETURNING id
'''),
                           {"user_id": user_id, "product_id": product_id})
                inserted_id = result.scalar()
                if inserted_id:
                    print(f"Wish added successfully: {inserted_id}")
                    return True
                else:
                    print("No result returned from insert operation")
                    return False
        except IntegrityError as e:
            print(f"IntegrityError: {str(e)}")
            return False
        except Exception as e:
            print(f"Error adding wish: {str(e)}")
            print(traceback.format_exc())
            return False

    @staticmethod
    def remove_wish(user_id, product_id):
        try:
            with app.db.engine.begin() as conn:
                result = conn.execute(text('''
DELETE FROM Wishes
WHERE user_id = :user_id AND product_id = :product_id
RETURNING id
'''),
                           {"user_id": user_id, "product_id": product_id})
                deleted_id = result.scalar()
                if deleted_id:
                    print(f"Wish removed successfully: {deleted_id}")
                    return True
                else:
                    print("No wish found to remove")
                    return False
        except Exception as e:
            print(f"Error removing wish: {str(e)}")
            return False
