from werkzeug.security import generate_password_hash
import csv
from faker import Faker
import random
from datetime import datetime, timedelta
import os
from tqdm import tqdm
import colorama
import argparse
colorama.init()

# Add after imports but before other code
def parse_args():
    parser = argparse.ArgumentParser(description='Generate dataset for Mini Amazon')
    parser.add_argument('--test', action='store_true', 
                      help='Run in test mode with smaller dataset')
    return parser.parse_args()

# Add after imports but before functions
def get_dataset_sizes(test_mode=False):
    if test_mode:
        return {
            'num_users': 20,
            'num_products': 50,
            'num_purchases': 30,
            'num_orders': 25,
            'num_order_items': 40,
            'num_cart_items': 15,
            'num_wishes': 20,
            'num_feedback': 25,
            'num_inventory': 30,
            'num_addresses': 15,
            'num_balance_transactions': 20
        }
    else:
        return {
            'num_users': 1000,
            'num_products': 5000,
            'num_purchases': 10000,
            'num_orders': 8000,
            'num_order_items': 15000,
            'num_cart_items': 3000,
            'num_wishes': 5000,
            'num_feedback': 7000,
            'num_inventory': 6000,
            'num_addresses': 2000,
            'num_balance_transactions': 5000
        }

# Increase numbers for larger dataset
num_users = 1000
num_products = 5000
num_purchases = 10000
num_orders = 8000
num_order_items = 15000
num_cart_items = 3000
num_wishes = 5000
num_feedback = 7000
num_inventory = 6000
num_addresses = 2000
num_balance_transactions = 5000

Faker.seed(0)
fake = Faker()

def get_csv_writer(f):
    return csv.writer(f, dialect='unix', quoting=csv.QUOTE_MINIMAL)

def read_existing_data(filename):
    data = []
    try:
        with open(f'../data/{filename}', 'r') as f:
            reader = csv.reader(f, dialect='unix')
            for row in reader:
                data.append(row)
    except FileNotFoundError:
        pass  # Silently handle missing files
    return data

def create_progress_bar(total, desc):
    """Create a consistently formatted progress bar"""
    return tqdm(
        total=total,
        desc=f"✨ {desc:15}",
        bar_format="{desc}: {percentage:3.0f}%|{bar:30}{r_bar}",
        colour='green',
        ncols=100,
        unit=' items',
        leave=True
    )

def gen_users(num_users, progress_bar=None):
    existing_users = read_existing_data('Users.csv')
    existing_ids = {int(user[0]) for user in existing_users}
    existing_emails = {user[1] for user in existing_users}  # Track existing emails
    next_id = max(existing_ids) + 1 if existing_ids else 0
    
    with open('Users.csv', 'w') as f:
        writer = get_csv_writer(f)
        
        # Write existing users
        for user in existing_users:
            writer.writerow(user)
        
        # Generate new users up to the target number
        for _ in range(num_users - len(existing_users)):
            while True:
                profile = fake.profile()
                email = profile['mail']
                if email not in existing_emails:  # Check for unique email
                    break
            
            existing_emails.add(email)  # Add new email to set
            plain_password = f'pass{next_id}'
            password = generate_password_hash(plain_password)
            name_components = profile['name'].split(' ')
            firstname = name_components[0]
            lastname = name_components[-1]
            writer.writerow([next_id, email, password, firstname, lastname])
            next_id += 1
            if progress_bar:
                progress_bar.update(1)

def gen_products(num_products, progress_bar=None):
    existing_products = read_existing_data('Products.csv')
    existing_ids = {int(product[0]) for product in existing_products}
    existing_names = {product[1] for product in existing_products}  # Track existing names
    next_id = max(existing_ids) + 1 if existing_ids else 0
    
    categories = ['Electronics', 'Books', 'Clothing', 'Food', 'Home', 'Sports', 'Toys']
    available_pids = [int(p[0]) for p in existing_products if p[-1].lower() == 'true']
    
    with open('Products.csv', 'w') as f:
        writer = get_csv_writer(f)
        
        # Write existing products
        for product in existing_products:
            writer.writerow(product)
        
        # Generate new products up to the target number
        for _ in range(num_products - len(existing_products)):
            while True:
                name = fake.catch_phrase().replace(',', '').replace('"', '').replace("'", '')
                if name not in existing_names:  # Check for unique name
                    break
            
            existing_names.add(name)  # Add new name to set
            price = f'{str(fake.random_int(max=10000))}.{fake.random_int(max=99):02}'
            description = fake.text(max_nb_chars=100).replace(',', '').replace('"', '').replace("'", '')
            image = 'NULL'
            category = random.choice(categories)
            available = 'true'
            if available == 'true':
                available_pids.append(next_id)
            writer.writerow([next_id, name, price, description, image, category, available])
            next_id += 1
            if progress_bar:
                progress_bar.update(1)
    
    return available_pids

def get_valid_user_ids():
    """Get a list of valid user IDs from Users.csv"""
    existing_users = read_existing_data('Users.csv')
    return [int(user[0]) for user in existing_users]

def gen_cart_items(num_cart_items, available_pids, progress_bar=None):
    existing_items = read_existing_data('Cart_Items.csv')
    seen = {(int(item[0]), int(item[1])) for item in existing_items}
    valid_users = get_valid_user_ids()
    
    with open('Cart_Items.csv', 'w') as f:
        writer = get_csv_writer(f)
        
        # Write existing items
        for item in existing_items:
            writer.writerow(item)
        
        # Generate new items
        for _ in range(len(existing_items), num_cart_items):
            while True:
                user_id = fake.random_element(elements=valid_users)  # Use valid user ID
                product_id = fake.random_element(elements=available_pids)
                if (user_id, product_id) not in seen:
                    seen.add((user_id, product_id))
                    break
            quantity = fake.random_int(min=1, max=5)
            saved_for_later = str(fake.boolean()).lower()
            writer.writerow([user_id, product_id, quantity, saved_for_later])
            if progress_bar:
                progress_bar.update(1)

def gen_orders(num_orders, progress_bar=None):
    existing_orders = read_existing_data('Orders.csv')
    existing_ids = {int(order[0]) for order in existing_orders}
    next_id = max(existing_ids) + 1 if existing_ids else 0
    valid_users = get_valid_user_ids()
    
    with open('Orders.csv', 'w') as f:
        writer = get_csv_writer(f)
        
        # Write existing orders
        for order in existing_orders:
            writer.writerow(order)
        
        # Generate new orders
        for _ in range(num_orders - len(existing_orders)):
            uid = fake.random_element(elements=valid_users)
            total_price = round(random.uniform(1, 10000), 2)
            time_purchased = fake.date_time_between(start_date='-1y', end_date='now').strftime('%Y-%m-%d %H:%M:%S')
            status = fake.random_element(elements=('Pending', 'Fulfilled', 'Cancelled'))
            writer.writerow([next_id, uid, total_price, time_purchased, status])
            next_id += 1
            if progress_bar:
                progress_bar.update(1)
    return next_id - 1  # Return the last order ID

def gen_purchases(num_purchases, available_pids, progress_bar=None):
    existing_purchases = read_existing_data('Purchases.csv')
    existing_ids = {int(purchase[0]) for purchase in existing_purchases}
    next_id = max(existing_ids) + 1 if existing_ids else 0
    
    # Get valid user IDs
    existing_users = read_existing_data('Users.csv')
    valid_user_ids = {int(user[0]) for user in existing_users}
    
    with open('Purchases.csv', 'w') as f:
        writer = get_csv_writer(f)
        
        # Write existing purchases
        for purchase in existing_purchases:
            writer.writerow(purchase)
        
        # Generate new purchases
        for id in range(next_id, num_purchases):
            uid = fake.random_element(elements=list(valid_user_ids))  # Only use valid user IDs
            pid = fake.random_element(elements=available_pids)
            time_purchased = fake.date_time_between(start_date='-2y', end_date='now')
            writer.writerow([id, uid, pid, time_purchased])
            if progress_bar:
                progress_bar.update(1)

def gen_wishes(num_wishes, available_pids, progress_bar=None):
    existing_wishes = read_existing_data('Wishes.csv')
    existing_ids = {int(wish[0]) for wish in existing_wishes}
    next_id = max(existing_ids) + 1 if existing_ids else 0
    seen = {(int(wish[1]), int(wish[2])) for wish in existing_wishes}
    valid_users = get_valid_user_ids()
    
    with open('Wishes.csv', 'w') as f:
        writer = get_csv_writer(f)
        
        # Write existing wishes - only first 3 columns
        for wish in existing_wishes:
            if (int(wish[1]), int(wish[2])) not in seen:  # Skip duplicates
                writer.writerow([wish[0], wish[1], wish[2]])  # Only id, user_id, product_id
                seen.add((int(wish[1]), int(wish[2])))
        
        # Generate new wishes
        for id in range(next_id, num_wishes):
            attempts = 0
            while attempts < 100:  # Limit attempts to avoid infinite loop
                user_id = fake.random_element(elements=valid_users)
                product_id = fake.random_element(elements=available_pids)
                if (user_id, product_id) not in seen:
                    seen.add((user_id, product_id))
                    writer.writerow([id, user_id, product_id])
                    if progress_bar:
                        progress_bar.update(1)
                    break
                attempts += 1

def gen_inventory(num_inventory, available_pids, progress_bar=None):
    existing_inventory = read_existing_data('Inventory.csv')
    seen = {(int(inv[0]), int(inv[1])) for inv in existing_inventory}
    valid_users = get_valid_user_ids()
    
    with open('Inventory.csv', 'w') as f:
        writer = get_csv_writer(f)
        
        # Write existing inventory
        for inv in existing_inventory:
            writer.writerow(inv)
        
        # Generate new inventory
        for _ in range(len(existing_inventory), num_inventory):
            while True:
                user_id = fake.random_element(elements=valid_users)
                product_id = fake.random_element(elements=available_pids)
                if (user_id, product_id) not in seen:
                    seen.add((user_id, product_id))
                    break
            quantity = fake.random_int(min=0, max=100)
            writer.writerow([user_id, product_id, quantity])
            if progress_bar:
                progress_bar.update(1)

def gen_feedback(num_feedback, available_pids, progress_bar=None):
    existing_feedback = read_existing_data('Feedback.csv')
    existing_ids = {int(feedback[0]) for feedback in existing_feedback}
    next_id = max(existing_ids) + 1 if existing_ids else 0
    
    with open('Feedback.csv', 'w') as f:
        # Write existing feedback exactly as is (without quotes)
        for feedback in existing_feedback:
            # Keep original format without adding quotes to the comment
            line = f"{feedback[0]}, {feedback[1]}, {feedback[2]}, {feedback[3]}, {feedback[4]}, {feedback[5]}\n"
            f.write(line)
        
        # Generate new feedback up to the target number (with quotes around comments)
        for _ in range(num_feedback - len(existing_feedback)):
            uid = fake.random_int(min=0, max=num_users-1)
            pid = fake.random_element(elements=available_pids)
            sid = fake.random_int(min=0, max=num_users-1)
            # Add quotes around the new review text
            review = fake.text(max_nb_chars=50).replace(',', '').replace('"', '').replace("'", '')
            time_reviewed = fake.date_time_between(start_date='-2y', end_date='now')
            line = f"{next_id}, {uid}, {pid}, {sid}, \"{review}\", {time_reviewed}\n"
            f.write(line)
            next_id += 1
            if progress_bar:
                progress_bar.update(1)

def gen_addresses(num_addresses, progress_bar=None):
    existing_addresses = read_existing_data('Addresses.csv')
    existing_ids = {int(addr[0]) for addr in existing_addresses} if existing_addresses else set()
    next_id = max(existing_ids) + 1 if existing_ids else 0
    valid_users = get_valid_user_ids()
    
    # Track users who already have a default address
    users_with_default = set()
    
    # First, write existing addresses and track users with default addresses
    with open('Addresses.csv', 'w') as f:
        writer = get_csv_writer(f)
        
        # Write existing addresses and track default addresses
        for addr in existing_addresses:
            writer.writerow(addr)
            if addr[6].lower() == 'true':  # If is_default is true
                users_with_default.add(int(addr[1]))  # Add user_id to set
    
    # Continue writing new addresses
    with open('Addresses.csv', 'a') as f:  # Open in append mode
        writer = get_csv_writer(f)
        
        # Generate new addresses
        for id in range(next_id, num_addresses):
            user_id = fake.random_element(elements=valid_users)
            street = fake.street_address().replace(',', '').replace('"', '').replace("'", '')
            city = fake.city().replace(',', '').replace('"', '').replace("'", '')
            state = fake.state().replace(',', '').replace('"', '').replace("'", '')
            zip_code = fake.zipcode()
            
            # Set default status - only if user doesn't have a default address yet
            if user_id not in users_with_default:
                is_default = 'true'
                users_with_default.add(user_id)
            else:
                is_default = 'false'
            
            writer.writerow([id, user_id, street, city, state, zip_code, is_default])
            if progress_bar:
                progress_bar.update(1)

def gen_order_items(num_order_items, available_pids, progress_bar=None):
    existing_items = read_existing_data('Order_Items.csv')
    seen = {(int(item[0]), int(item[1])) for item in existing_items}
    
    # Get valid order IDs from Orders table (not Orders_Buy)
    orders = read_existing_data('Orders.csv')
    valid_order_ids = [int(order[0]) for order in orders]
    
    with open('Order_Items.csv', 'w') as f:
        writer = get_csv_writer(f)
        
        # Write existing order items
        for item in existing_items:
            writer.writerow(item)
        
        # Generate new order items
        for _ in range(len(existing_items), num_order_items):
            while True:
                order_id = fake.random_element(elements=valid_order_ids)
                product_id = fake.random_element(elements=available_pids)
                if (order_id, product_id) not in seen:
                    seen.add((order_id, product_id))
                    break
            
            quantity = fake.random_int(min=1, max=10)
            fulfilled = str(fake.boolean()).lower()
            # Use empty string for NULL timestamps
            fulfillment_date = fake.date_time_between(start_date='-1y', end_date='now').strftime('%Y-%m-%d %H:%M:%S') if fulfilled == 'true' else ''
            unit_price = round(random.uniform(1, 1000), 2)
            writer.writerow([order_id, product_id, quantity, fulfilled, fulfillment_date, unit_price])
            if progress_bar:
                progress_bar.update(1)

def gen_balance_transactions(num_transactions, progress_bar=None):
    existing_transactions = read_existing_data('BalanceTransactions.csv')
    existing_ids = {int(trans[0]) for trans in existing_transactions} if existing_transactions else set()
    next_id = max(existing_ids) + 1 if existing_ids else 0
    valid_users = get_valid_user_ids()
    
    with open('BalanceTransactions.csv', 'w') as f:
        writer = get_csv_writer(f)
        
        # Write existing transactions
        for trans in existing_transactions:
            writer.writerow(trans)
        
        # Generate new transactions
        for id in range(next_id, num_transactions):
            user_id = fake.random_element(elements=valid_users)  # Use valid user ID
            amount = round(random.uniform(-1000, 1000), 2)
            transaction_type = 'deposit' if amount > 0 else 'withdraw'
            timestamp = fake.date_time_between(start_date='-1y', end_date='now')
            writer.writerow([id, user_id, amount, transaction_type, timestamp])
            if progress_bar:
                progress_bar.update(1)

def gen_ordered_items_info(num_ordered_items, available_pids, progress_bar=None):
    existing_items = read_existing_data('Ordered_Items_Info.csv')
    existing_ids = {int(item[0]) for item in existing_items}
    next_id = max(existing_ids) + 1 if existing_ids else 0
    valid_users = get_valid_user_ids()
    
    with open('Ordered_Items_Info.csv', 'w') as f:
        writer = get_csv_writer(f)
        
        # Write existing items
        for item in existing_items:
            writer.writerow(item)
        
        # Generate new items
        for _ in range(num_ordered_items - len(existing_items)):
            date_order_placed = fake.date_time_between(start_date='-1y', end_date='now')
            fulfilled = str(fake.boolean()).lower()
            buyer_id = fake.random_element(elements=valid_users)  # Use valid user ID
            seller_id = fake.random_element(elements=valid_users)  # Use valid user ID
            product_id = fake.random_element(elements=available_pids)
            total_items = fake.random_int(min=1, max=10)
            buyer_address = fake.address().replace(',', '').replace('"', '').replace("'", '')
            
            writer.writerow([next_id, date_order_placed, fulfilled, buyer_id, seller_id, 
                           product_id, total_items, buyer_address])
            next_id += 1
            if progress_bar:
                progress_bar.update(1)

def main():
    args = parse_args()
    sizes = get_dataset_sizes(args.test)
    
    print("\n🚀 Starting Large Dataset Generation...\n")
    print(f"{'🧪 TEST MODE' if args.test else '📊 FULL MODE'} - Generating data...\n")
    
    # Define generation steps in correct order
    generation_steps = [
        (gen_users, [sizes['num_users']], "👥 Users"),
        (gen_products, [sizes['num_products']], "📦 Products"),
        (gen_orders, [sizes['num_orders']], "📝 Orders"),  # Generate orders before order items
        (gen_order_items, [sizes['num_order_items']], "📋 Order Items"),
        (gen_purchases, [sizes['num_purchases']], "💰 Purchases"),
        (gen_cart_items, [sizes['num_cart_items']], "🛒 Cart Items"),
        (gen_wishes, [sizes['num_wishes']], "⭐ Wishes"),
        (gen_inventory, [sizes['num_inventory']], "📦 Inventory"),
        (gen_feedback, [sizes['num_feedback']], "💭 Feedback"),
        (gen_addresses, [sizes['num_addresses']], "📍 Addresses"),
        (gen_balance_transactions, [sizes['num_balance_transactions']], "💳 Transactions"),
        (gen_ordered_items_info, [sizes['num_order_items']], "📦 Ordered Items Info")
    ]
    
    # Read existing data counts using the same descriptions as generation_steps
    existing_counts = {}
    for _, _, desc in generation_steps:
        if desc == "📦 Ordered Items Info":
            existing_counts[desc] = len(read_existing_data('Ordered_Items_Info.csv'))
        else:
            filename = desc[2:].strip().replace(' ', '_') + '.csv'  # Convert emoji description to filename
            existing_counts[desc] = len(read_existing_data(filename))
    
    # Initialize all progress bars with correct totals
    progress_bars = {}
    for _, args, desc in generation_steps:
        existing_count = existing_counts[desc]
        target_count = args[0]
        
        # Calculate remaining items to generate
        remaining = target_count - existing_count
        
        pbar = tqdm(
            total=remaining,  # Use the actual number of items we need to generate
            desc=f"{desc:20}",
            bar_format="{desc} |{bar:30}| {percentage:3.0f}% | {n_fmt}/{total_fmt}",
            colour='green',
            leave=True,
            position=len(progress_bars)
        )
        
        # If we don't need to generate any new items, show as complete
        if remaining <= 0:
            pbar.total = 1
            pbar.update(1)
        
        progress_bars[desc] = pbar
    
    # Create overall progress bar at the bottom
    main_pbar = tqdm(
        total=len(generation_steps),
        desc="🔄 Overall Progress",
        bar_format="{desc} |{bar:30}| {percentage:3.0f}% | {n_fmt}/{total_fmt} tasks",
        colour='blue',
        position=len(progress_bars)  # Put it at the bottom
    )
    
    # Track available_pids for functions that need it
    available_pids = None
    
    # Execute each generation step
    for func, args, desc in generation_steps:
        current_pbar = progress_bars[desc]
        
        try:
            if func == gen_products:
                available_pids = func(*args, progress_bar=current_pbar)
            elif func in (gen_purchases, gen_cart_items, gen_order_items, 
                        gen_wishes, gen_inventory, gen_feedback, 
                        gen_ordered_items_info):
                func(*args, available_pids, progress_bar=current_pbar)
            else:
                func(*args, progress_bar=current_pbar)
        except Exception as e:
            print(f"\nError in {desc}: {str(e)}")
            raise e
            
        main_pbar.update(1)
    
    # Close all progress bars
    for pbar in progress_bars.values():
        pbar.close()
    main_pbar.close()
    
    # Calculate actual total of new items generated
    total_new_items = sum(max(0, args[0] - existing_counts[desc]) for _, args, desc in generation_steps)
    
    print("\n✅ Data generation completed successfully!")
    print(f"📈 Total items generated: {total_new_items:,}")
    print("🎉 Your large dataset is ready!\n")

if __name__ == '__main__':
    main()