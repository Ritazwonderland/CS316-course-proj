from flask_login import UserMixin
from flask import current_app as app, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import traceback
from sqlalchemy import text
from app.models.address import Address
from app.models.balance import BalanceTransaction

class User(UserMixin):
    def __init__(self, id, email, firstname, lastname):
        self.id = id
        self.email = email
        self.firstname = firstname
        self.lastname = lastname

    def check_password(self, password):
        user_data = app.db.execute("""
SELECT password
FROM Users
WHERE id = :id
""",
                                   {"id": self.id})
        if user_data:
            stored_password = user_data[0][0]
            return check_password_hash(stored_password, password)
        return False

    def set_password(self, password):
        hashed_password = generate_password_hash(password)
        try:
            with app.db.engine.begin() as conn:
                conn.execute(text("""
UPDATE Users
SET password = :password
WHERE id = :id
"""),
                             {"password": hashed_password, "id": self.id})
            print(f"Password updated successfully for user {self.id}")
        except Exception as e:
            print(f"Error updating password for user {self.id}: {str(e)}")
            raise

    @staticmethod
    def get_by_auth(email, password):
        rows = app.db.execute("""
SELECT password, id, email, firstname, lastname
FROM Users
WHERE email = :email
""",
                              {"email": email})
        if not rows:  # email not found
            return None
        elif not check_password_hash(rows[0][0], password):
            # incorrect password
            return None
        else:
            return User(*(rows[0][1:]))

    @staticmethod
    def email_exists(email):
        rows = app.db.execute("""
SELECT email
FROM Users
WHERE email = :email
""",
                              {"email": email})
        return len(rows) > 0

    @staticmethod
    def register(email, password, firstname, lastname):
        try:
            with app.db.engine.begin() as conn:
                result = conn.execute(text("""
INSERT INTO Users(email, password, firstname, lastname)
VALUES(:email, :password, :firstname, :lastname)
RETURNING id
"""),
                                      {"email": email,
                                       "password": generate_password_hash(password),
                                       "firstname": firstname,
                                       "lastname": lastname})
                id = result.fetchone()[0]
                print(f"New user registered with id: {id}")  # Debug print
                
                # Fetch the user within the same transaction
                result = conn.execute(text("""
SELECT id, email, firstname, lastname
FROM Users
WHERE id = :id
"""),
                                      {"id": id})
                user_data = result.fetchone()
                if user_data:
                    print(f"Successfully retrieved new user: {user_data.email}")  # Debug print
                    return User(*user_data)
                else:
                    print(f"Failed to retrieve new user with id: {id}")  # Debug print
                    return None
        except Exception as e:
            print(f"Error in User.register: {str(e)}")
            print(traceback.format_exc())
            return None

    @staticmethod
    def get(id):
        print(f"User.get() called with id: {id}")  # Debug print
        print(f"Type of id: {type(id)}")  # Debug print
        rows = app.db.execute("""
SELECT id, email, firstname, lastname
FROM Users
WHERE id = :id
""",
                              {"id": int(id)})  # Ensure id is an integer
        print(f"Query result: {rows}")  # Debug print
        if rows:
            user = User(*rows[0])
            print(f"Retrieved user: {user.id}, {user.email}")  # Debug print
            return user
        else:
            print(f"No user found with id: {id}")  # Debug print
            return None

    def get_addresses(self):
        try:
            addresses = Address.get_all_by_user_id(self.id)
            print(f"Retrieved addresses for user {self.id}: {addresses}")  # Debug print
            return addresses
        except Exception as e:
            print(f"Error getting addresses for user {self.id}: {str(e)}")
            return []

    @staticmethod
    def get_by_email(email):
        rows = app.db.execute("""
        SELECT id, email, firstname, lastname
        FROM Users
        WHERE email = :email
        """,
                              {"email": email})
        return User(*(rows[0])) if rows else None

    def get_avatar_url(self):
        # In the future, you can add logic here to return a custom avatar if the user has set one
        return url_for('static', filename='images/default_avatar.png')

    def get_balance(self):
        return BalanceTransaction.get_balance(self.id)

    def add_funds(self, amount):
        return BalanceTransaction.add_transaction(self.id, amount, 'add')

    def withdraw_funds(self, amount):
        current_balance = self.get_balance()
        if current_balance >= amount:
            return BalanceTransaction.add_transaction(self.id, amount, 'withdraw')
        return None
