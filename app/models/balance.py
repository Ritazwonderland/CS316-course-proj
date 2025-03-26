from flask import current_app as app
from sqlalchemy import text

class BalanceTransaction:
    def __init__(self, id, user_id, amount, transaction_type, timestamp):
        self.id = id
        self.user_id = user_id
        self.amount = amount
        self.transaction_type = transaction_type
        self.timestamp = timestamp

    @staticmethod
    def add_transaction(user_id, amount, transaction_type):
        try:
            with app.db.engine.begin() as conn:
                result = conn.execute(text('''
INSERT INTO BalanceTransactions(user_id, amount, transaction_type)
VALUES(:user_id, :amount, :transaction_type)
RETURNING id
'''),
                           {"user_id": user_id, "amount": amount, "transaction_type": transaction_type})
                transaction_id = result.scalar()
                print(f"Added transaction: user_id={user_id}, amount=${amount:.2f}, type={transaction_type}, id={transaction_id}")
                return transaction_id
        except Exception as e:
            print(f"Error adding balance transaction: {str(e)}")
            return None

    @staticmethod
    def get_balance(user_id):
        try:
            result = app.db.execute('''
SELECT COALESCE(SUM(CASE WHEN transaction_type = 'add' THEN amount ELSE -amount END), 0) as balance
FROM BalanceTransactions
WHERE user_id = :user_id
''',
                           {"user_id": user_id})
            balance = result[0][0] if result else 0  # Get the first column of the first row
            print(f"Retrieved balance for user {user_id}: ${balance:.2f}")
            return balance
        except Exception as e:
            print(f"Error getting balance for user {user_id}: {str(e)}")
            return 0
