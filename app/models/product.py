from flask import current_app as app
from sqlalchemy import text

#categories = ['Electronics', 'Books', 'Clothing', 'Food', 'Home', 'Sports', 'Toys']
class Product:
    def __init__(self, id, name, price, description, image, category, available):
        self.id = id
        self.name = name
        self.price = price
        self.description = description
        self.image = image
        self.category = category
        self.available = available

    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT id, name, price, description, image, category, available
FROM Products
WHERE id = :id
''',
                              {"id": id})
        return Product(*(rows[0])) if rows else None
    @staticmethod
    def getInventory(pid):
        from .inventory import Inventory
        rows = app.db.execute('''
SELECT user_id, product_id, quantity
FROM Inventory
WHERE product_id = :pid
''',
                              {"pid": pid})
        return [Inventory(*row) for row in rows]

    @staticmethod
    def getFeedback(pid):
        from .modelFeedback import Feedback
        rows = app.db.execute('''
SELECT *
FROM Feedback


''',
                              {"id": pid})
        return [Feedback(*row) for row in rows]


    @staticmethod
    def get_all(available=True):
        rows = app.db.execute('''
SELECT id, name, price, description, image, category, available
FROM Products
WHERE available = :available
''',
                              {"available": available})
        return [Product(*row) for row in rows]

    @staticmethod
    def get_top_expensive(k, available=True):
        rows = app.db.execute('''
SELECT id, name, price, description, image, category, available
FROM Products
WHERE available = :available
ORDER BY price DESC
LIMIT :k
''', {"available":available, "k": k})
        return [Product(*row) for row in rows]

    @staticmethod
    def search(name, category,available=True):
        if category == 'None':
            rows = app.db.execute('''
SELECT id, name, price, description, image, category, available
FROM Products
WHERE available = :available
AND name ILIKE :name
ORDER BY price ASC
LIMIT 15
''', {"available":available, "name": f"%{name}%"})
        else:
            rows = app.db.execute('''
SELECT id, name, price, description, image, category, available
FROM Products
WHERE available = :available
AND name ILIKE :name
AND category = :category
ORDER BY price ASC
LIMIT 15
''', {"available":available, "name": f"%{name}%" , "category": category})
        #print(rows)
        return [Product(*row) for row in rows]


    @staticmethod
    def getList(uid):
        from .inventory import Inventory
        rows = app.db.execute('''
SELECT product_id
FROM Inventory
WHERE user_id = :uid
''',{"uid": uid})
        return Inventory(*(rows[0])) if rows else None
        
            
