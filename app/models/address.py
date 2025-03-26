from flask import current_app as app
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text

class Address:
    def __init__(self, id, user_id, street, city, state, zip_code, is_default):
        self.id = id
        self.user_id = user_id
        self.street = street
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.is_default = is_default

    @staticmethod
    def get_all_by_user_id(user_id):
        print(f"Fetching addresses for user_id: {user_id}")  # Debug print
        try:
            rows = app.db.execute('''
SELECT id, user_id, street, city, state, zip_code, is_default
FROM Addresses
WHERE user_id = :user_id
''',
                                  {"user_id": user_id})
            print(f"Fetched rows: {rows}")  # Debug print
            addresses = [Address(*row) for row in rows]
            print(f"Returning addresses: {addresses}")  # Debug print
            return addresses
        except Exception as e:
            print(f"Error fetching addresses: {str(e)}")
            return []

    @staticmethod
    def add_address(user_id, street, city, state, zip_code, is_default=False):
        try:
            print(f"Preparing to add address for user_id: {user_id}")  # Debug print
            print(f"Address details: street={street}, city={city}, state={state}, zip_code={zip_code}, is_default={is_default}")  # Debug print
            with app.db.engine.begin() as conn:
                print("Database connection established.")  # Debug print
                if is_default:
                    # If this is the new default, unset any existing default
                    conn.execute(text('''
UPDATE Addresses SET is_default = FALSE WHERE user_id = :user_id
'''), {"user_id": user_id})
                result = conn.execute(text('''
INSERT INTO Addresses(user_id, street, city, state, zip_code, is_default)
VALUES(:user_id, :street, :city, :state, :zip_code, :is_default)
RETURNING id
'''), {
                    "user_id": user_id,
                    "street": street,
                    "city": city,
                    "state": state,
                    "zip_code": zip_code,
                    "is_default": is_default
                })
                id = result.scalar()
                print(f"New address added with id: {id}")  # Debug print
                
                # Verify the insertion by fetching the newly added record
                verify_result = conn.execute(text('''
SELECT id, user_id, street, city, state, zip_code, is_default
FROM Addresses
WHERE id = :id
'''), {"id": id})
                verified_row = verify_result.fetchone()
                if verified_row:
                    print(f"Verified new address: {verified_row}")  # Debug print
                    return Address(*verified_row)
                else:
                    print("Failed to verify new address")  # Debug print
                    return None
        except SQLAlchemyError as e:
            print(f"SQLAlchemy error adding address: {str(e)}")
            return None
        except Exception as e:
            print(f"Unexpected error adding address: {str(e)}")
            return None

    @staticmethod
    def get(id):
        try:
            rows = app.db.execute('''
                SELECT id, user_id, street, city, state, zip_code, is_default
                FROM Addresses
                WHERE id = :id
            ''', {'id': id})
            
            print(f"Fetched rows for id {id}: {rows}")  # Debug print
            
            if not rows:  # No rows found
                print(f"No address found with id: {id}")
                return None
                
            row = rows[0] if isinstance(rows, list) else rows.fetchone()
            if not row:  # No row data
                print(f"No row data found for id: {id}")
                return None
                
            print(f"Using row: {row}")  # Debug print
            return Address(*row)
            
        except Exception as e:
            print(f"Error getting address: {str(e)}")
            return None

    @staticmethod
    def set_default(address_id, user_id):
        try:
            with app.db.engine.begin() as conn:
                # Unset any existing default
                conn.execute(text('''
UPDATE Addresses SET is_default = FALSE WHERE user_id = :user_id
'''), {"user_id": user_id})
                # Set the new default
                conn.execute(text('''
UPDATE Addresses SET is_default = TRUE WHERE id = :id AND user_id = :user_id
'''), {"id": address_id, "user_id": user_id})
            return True
        except SQLAlchemyError as e:
            print(f"Error setting default address: {str(e)}")
            return False

    @staticmethod
    def get_default(user_id):
        try:
            row = app.db.execute('''
SELECT id, user_id, street, city, state, zip_code, is_default
FROM Addresses
WHERE user_id = :user_id AND is_default = TRUE
''',
                                 {"user_id": user_id}).fetchone()
            return Address(*row) if row else None
        except SQLAlchemyError as e:
            print(f"Error fetching default address: {str(e)}")
            return None

    def __repr__(self):
        return f"<Address {self.id}: {self.street}, {self.city}, {self.state} {self.zip_code} (Default: {self.is_default})>"

    @staticmethod
    def delete(address_id):
        try:
            with app.db.engine.begin() as conn:
                result = conn.execute(text('''
DELETE FROM Addresses
WHERE id = :id
RETURNING id
'''), {"id": address_id})
                deleted_id = result.scalar()
                if deleted_id:
                    print(f"Address deleted successfully: {deleted_id}")
                    return True
                else:
                    print(f"No address found with id: {address_id}")
                    return False
        except SQLAlchemyError as e:
            print(f"Error deleting address: {str(e)}")
            return False

    @staticmethod
    def update(address):
        try:
            with app.db.engine.begin() as conn:
                # If setting as default, first unset any existing default
                if address.is_default:
                    conn.execute(text('''
                        UPDATE Addresses 
                        SET is_default = false 
                        WHERE user_id = :user_id AND is_default = true
                    '''), {"user_id": address.user_id})

                # Update the address
                result = conn.execute(text('''
                    UPDATE Addresses
                    SET street = :street,
                        city = :city,
                        state = :state,
                        zip_code = :zip_code,
                        is_default = :is_default
                    WHERE id = :id
                    AND user_id = :user_id
                    RETURNING id
                '''), {
                    "id": address.id,
                    "user_id": address.user_id,
                    "street": address.street,
                    "city": address.city,
                    "state": address.state,
                    "zip_code": address.zip_code,
                    "is_default": address.is_default
                })
                
                # Get the returned id
                updated_id = result.scalar()
                return bool(updated_id)
                
        except Exception as e:
            print(f"Error updating address: {str(e)}")
            return False
