---

# Owned by Backlog Bashers as part of course project for CS316 2024FALL
# Drafted by Juntang at Sep 22, 2024 

---

---

# REPORT.pdf - **Account / Purchases** (Users Guru)

---

## 1. **Database Design**

### **Tables:**

#### 1. **Users Table**
- **Purpose**: Stores all user account information for login and profile management.
- **Columns**:
   - `user_id`: INT, **Primary Key**, system-generated unique identifier for each user.
   - `email`: VARCHAR(255), **Unique**, stores user email for login.
   - `full_name`: VARCHAR(255), stores the full name of the user.
   - `address`: TEXT, stores the user’s shipping address.
   - `password`: VARCHAR(255), stores the user's encrypted password.
   - `balance`: DECIMAL(10, 2), **Default = 0**, stores the user's current balance in virtual currency.
- **Constraints**:
   - `email` must be unique across the system to prevent duplicate registrations.
   - Passwords are stored securely using encryption algorithms such as bcrypt to ensure data security.
- **Indexes**:
   - Create an index on `email` for faster login lookups.

#### 2. **Purchase History Table**
- **Purpose**: Tracks all purchases made by users, capturing key purchase information such as order date, status, and total amount.
- **Columns**:
   - `purchase_id`: INT, **Primary Key**, unique identifier for each purchase.
   - `user_id`: INT, **Foreign Key** references `Users.user_id`, associating purchases with users.
   - `purchase_date`: DATE, records the date the purchase was made.
   - `total_amount`: DECIMAL(10, 2), stores the total value of the purchase.
   - `item_count`: INT, records the number of items in the purchase.
   - `status`: ENUM('Pending', 'Fulfilled', 'Cancelled'), stores the current status of the purchase.
- **Constraints**:
   - `user_id` must exist in the `Users` table to ensure referential integrity.
- **Indexes**:
   - Create an index on `user_id` for fast access to a user's purchase history.
   - Create a composite index on `purchase_date` and `user_id` for reverse chronological sorting.

#### 3. **User Profile View Table (Optional but Recommended)**
- **Purpose**: Stores public-facing user profile information for public display.
- **Columns**:
   - `user_id`: INT, **Foreign Key** references `Users.user_id`.
   - `profile_data`: TEXT, stores a concise summary of user details (e.g., full name, user ID, seller status).
   - `seller_reviews`: TEXT, aggregates reviews for sellers (if the user is also a seller).

### **Assumptions**:
- Users can update their name, address, and email, but the `user_id` is immutable.
- Each user starts with a $0 balance, which they can top up or withdraw at any time (within the system’s constraints).
- Users can only view and update their own account details.
- **Security Considerations**: All sensitive information such as passwords are encrypted, and email uniqueness is enforced via database constraints.

---

## 2. **User Flows and Page-by-Page Design**

### **Account Management**

#### **1. Registration Page**:
- **Purpose**: Allows new users to create an account.
- **Form Fields**:
   - Full Name
   - Email (Unique)
   - Address
   - Password (with encryption for storage)
- **Process**:
   1. User fills in the registration form.
   2. The system generates a unique `user_id` and stores the information in the `Users` table.
   3. If the email already exists, prompt the user with an error message.
   4. Upon successful registration, redirect the user to the login page.

#### **2. Login Page**:
- **Purpose**: Allows existing users to log in using their email and password.
- **Form Fields**:
   - Email
   - Password
- **Process**:
   1. User enters email and password.
   2. The system checks the email in the `Users` table and verifies the encrypted password.
   3. If credentials match, the user is logged in and redirected to their account dashboard.
   4. If invalid, an error message is displayed.

#### **3. Account Dashboard**:
- **Purpose**: Displays user account information and options to update their profile and manage their balance.
- **Content**:
   - User’s full name, email, and address.
   - Current balance, with options to **Top Up** or **Withdraw**.
   - Links to view **Purchase History** and **Public Profile**.
- **Process**:
   - Users can update their name, email, or address via editable fields.
   - Any changes are validated and updated in the `Users` table, except the immutable `user_id`.
   - Top up and withdrawal functionality will adjust the `balance` field accordingly, with constraints to ensure no overdraft.

---

### **Purchase History**

#### **1. Purchase History Page**:
- **Purpose**: Allows users to view a reverse chronological list of their past purchases.
- **Content**:
   - Summary of each purchase, showing the **purchase date**, **total amount**, **number of items**, and **status**.
   - Each purchase links to a **Detailed Order Page** for further information.
- **Process**:
   1. User clicks on "Purchase History" in their dashboard.
   2. The system retrieves all purchases from the `Purchase History` table using the `user_id` and displays them.
   3. Purchases are displayed in reverse chronological order.
   4. Users can click on individual purchases to view details.

#### **2. Detailed Order Page**:
- **Purpose**: Provides in-depth details of a specific order, including all items purchased and fulfillment status.
- **Content**:
   - For each item: Product name, quantity, price per item, and total for the line item.
   - Overall order details: Total amount, order date, status (Pending/Fulfilled/Cancelled), and fulfillment updates.
- **Process**:
   - Users access this page by clicking a purchase from their history.
   - The system fetches the detailed information from the `Purchase History`, `Order_Items`, and `Orders` tables.

---

### **Public Profile**

#### **1. Public User Profile Page**:
- **Purpose**: Provides a public-facing view of the user’s basic details and seller reviews (if applicable).
- **Content**:
   - Display: User's **account number** and **full name**.
   - If the user is also a seller, include **email**, **address**, and a section with **reviews for this seller**.
- **Process**:
   - Users access this page via public links (if allowed), and it fetches data from the `User Profile View` table.

---

### **Optional Enhancements (Future)**

1. **Search/Filter Purchase History**:
   - Users can search their purchase history by **item**, **seller**, or **date range** using additional query parameters.

2. **Balance and Purchase Visualization**:
   - Graphical representation of balance history, spending by category, and purchase trends.

---

# REPORT.pdf - **Products** (Product Guru)

## 1. **Database Design: Product**

### **Tables:**

#### 1. **Product Table**
- **Purpose**: Stores all product information.
- **Columns**:
   - `product_id`: INT, **Primary Key**, system-generated unique identifier for each product made by a user.
   - `Name`: VARCHAR(255), stores name of the product.
   - `Description`: TEXT, stores the full description of product entered by user
   - `Image`: IMAGE, stores the product's image.
   - `Category`: VARCHAR(255), stores the category that the product belongs to.
   - `price`: DECIMAL(10, 2), **Default = 0**, stores th product's price in the virtual currency.
- **Constraints**:
   - `Name` must be allow for duplicates as different users can sell the same product.
- **Search**:
   - Create an search sytem with `Name` and `Category` to find products quickly.

#### 2. **Product Page Table**
- **Purpose**: Stores all information on one product and display it.
- **Columns**:
   - `product_id`: INT, **Primary Key**, system-generated unique identifier for each product made by a user.
   - `Name`: VARCHAR(255), stores name of the product.
   - `Description`: TEXT, stores the full description of product entered by user
   - `Short Description`: TEXT, stores the abbreviated description of product entered by user
   - `Image`: IMAGE, stores the product's image.
   - `Category`: VARCHAR(255), stores the category that the product belongs to.
   - `price`: DECIMAL(10, 2), **Default = 0**, stores th product's price in the virtual currency.
   - `Sellers`: LIST/TUPLE, stores the list of sellers for that specific product and their quantity of product for each seller as a tuple
### **Assumptions**:
- Sellers can update the all attributes except the `product_id`.

---

## 2. **User Flows and Page-by-Page Design**

### **Product Search**
- **Purpose**: allows user to search for products by catergory, name, or price range
- **Form Fields**:
   - Name
   - Category
   - Price Range
- **Content**:
   - A list of products found based on the current search
   - For each product, displays the name, abbreviated desciription, image, and price
- **Process**:
   - User enters information about the product they desire
   - System fetches and displays a list of products and its image that match the category and name, as well as is within the price range
   - User can click on the product image to go to the product page 

### **Product page for Non-seller**
- **Purpose**: allows user to see the full description, price and images of a product, as well as the quantities each seller has of the product
- **Content**: 
   - Product full description, image, and price
   - list of sellers and their quantities of product
- **Process**:
   - System fetches and displays the full description, image, and price of products
   - System then fetches the list of sellers of the product and their associated quantities
   - User can click on add to cart button to add product to cart

### **Product page for Non-seller**
- **Purpose**: allows seller to update product attributes
- **Form Fields**:
   - Name
   - Category
   - Price
   - Description
   - Image
   - Quantity
- **Content**: 
   - Product full description, image, price, Category, and Quantity
- **Process**:
   - User can add or make changes to products
   - If product has not been created, system will add row to product and product page tables 
   - if product attributes are being changed, system will update row on the product and product page tables
   - if user wishes to delete product, system will remove row from product and product page tables for that user

# REPORT.pdf - **Feedback / Messaging** (Social Guru)

## 1. **Database Design**

### **Product Review Table**
- **Purpose**: Store ratings/reviews for individual products
- **Columns**: 
   - `User`: UID of customer submitting the rating/review
   - `Product`: ID/Name of product being reviewed
   - `Rating`: Numerical score given to product by user
   - `Review`: Description of product by user in words
   - `Date`: Day/Time when review was made or updated
- **Restrictions**: Key is given by `User` and `Product` since each user may only have 1 review for each product. The table must also be mutable so users can change their ratings and reviews

### **Seller Review Table**
- **Purpose**: Store ratings/reviews for sellers of products-- extremely similar in structure to product review table
- **Columns**: 
   - `User`: UID of customer submitting the rating/review
   - `Seller`: ID/Name of seller being reviewed
   - `Rating`: Numerical score given to seller by user
   - `Review`: Description of seller by user in words
   - `Date`: Day/Time when review was made or updated
- **Restrictions**: Key is similarly given by `User` and `Seller` since each user may only have 1 review for each seller. The table must also be mutable so users can change their ratings and reviews

- Above tables can (and almost certainly will) be filtered by User ID and inserted into a common third temporary table for each user to see their own ratings/reviews. Tables could also be combined using NULL values to make distinct products or sellers, if conciseness is desired.

### **Product Statistics Table**
- **Purpose**: Store information about summary statistics relating to products with regards to their ratings/reviews by users
- **Columns**: 
   - `Product`: ID/Name of product being summarized
   - `Num_Ratings`: Number of ratings given to this product
   - `Avg_Rating`: Average rating given to this product
- **Restrictions**: Key is simply `Product` since each product can only have one average rating

### **Seller Statistics Table**
- **Purpose**: Store information about summary statistics relating to products with regards to their ratings/reviews by users
- **Columns**: 
   - `Seller`: ID/Name of seller being summarized
   - `Num_Ratings`: Number of ratings given to this seller
   - `Avg_Rating`: Average rating given to this seller
- **Restrictions**: Key is simply `Seller` since each seller can only have one average rating

- Like before, above tables can be combined using NULL values to separate sellers and products if that path is desired

### **Possible Additional Tables/Modifications**

- Message Thread Table: Storing User and Seller IDs and possibly a list of strings, each string corresponding to a message sent by one to the other (somehow distinct depending on who sent it)

- Add column to product/seller review tables corresponding to upvotes by any and all users, using this table as the default sorting (desc) method for the top 3 reviews

- Somehow add a column to review tables for attached images to be displayed on the review page

## 2. **User Flow and Page-by-Page Design**

- Seller review page should be distinct from product review page, but each should have a similar interactable layout to avoid customer confusion.

- Product and seller reviews should be shown in distinct sections of product and seller detail pages, respectively (likely towards the bottom, read-only, but perhaps sortable by pressing certain columns).

- Link to make a review for a product can be found in the detailed product page, while links to make reviews for sellers can be found in order confirmation page (to ensure only paid customers can review a seller).

- Each user should be able to see their reviews on their own account page, where most recent reviews are shown first but can be sorted in similar fashion to product and seller reviews (described above). A user can also select an individual review they have made and be prompted to change or delete it.

# REPORT.pdf - **Cart/Order** (Carts Guru)

## 1. **Database Design**

### **Cart Items Table**
- **Purpose**: Store items an quantities in a user's cart/saved for later
- **Columns**: 
   - `user_id`: INT **Primary Key** **Foreign Key** references `Users.user_id`. Unique ID of the owner (user) of the cart
   - `product_id`: INT **Primary Key** **Foreign Key**   Unique ID/Name of product in cart
   - `quantity`: INT quanity of the item in the cart
   - `saved_for_later`: BOOL Whether the product in the cart is saved for later or not
- **Restrictions**: 
   - Key is given by `user_id` and `product_id` since each individual can only have one instance of a specific product in their cart; if there is more than one of said product, the quantity increases

### **Orders Table**
- **Purpose**: Store items an quantities in a user's cart/saved for later
- **Columns**: 
   - `order_id`: INT **Primary Key** Unique ID of the individual order submitted
   - `user_id`: INT **Foreign Key** references `Users.user_id`. Unique ID of the owner (user) of the order
   - `total_price` : DECIMAL(10, 2) Total price paid for order
   - `order_date`: DATETIME date and time of the order submission
   - `status`: VARCHAR(255) Whether the order is Pending/Fulfilled/Cancelled
- **Restrictions**: 
   - Key is given by `order_id` because each user can have multiple orders, but many individual products can be held wihtin each order
   - 

### **Order Items Table**
- **Purpose**: Store items from orders and their fulfillment status
- **Columns**: 
   - `order_id`: INT **Primary Key** **Foreign Key** references `Orders.order_id`Unique ID of the individual order submitted
   - `product_id`: INT **Primary Key** **Foreign Key** references `Product.product_id`. Unique ID/Name of product in order
   - `quantity`: INT quanity of the item in the cart
   - `unit_price` : DECIMAL(10, 2) price of an individual item
   - `fulfilled`: BOOL Whether the product has been fulfilled by seller or not
   - `fulfillment_date`: DATETIME date and time of the order has been fulfilled
- **Restrictions**: 
   - Key is given by `order_id` and `product_id` because there can be many products in every order and products can be in multiple orders.

   ### **Assumptions**:
- `total_price` is held in `Orders` because the unit prices of individual products may change over time, but this preserves the total amount the customer actually paid.
- `unit_price` is held in `Order_Items` because it captures the unit prices of a product at the time of purchase
- `order_id` is unique across all users because that allows for faster tracking of orders.
- `Orders.status`  changes based on the fulfillment status of the items. An order is pending when not all of the items are fulfilled. It is fulfilled when all items are fulfilled, and cancelled when the order is cancelled.
- `Order_Items.fulfillment_date` is true when all of the products have been fulfilled.

## 2. **User Flows and Page-by-Page Design**


#### **1. Cart Page**:
- **Purpose**: Allows users to view and manage items in their shopping cart, including those saved for later.
- **Content**
   Main cart section:
   - List of items with product name, quantity, unit price, and subtotal for each item.
   - Options to change quantity or remove items.
   - Running total of all items in the cart.
   Saved for Later section
   - List of items saved for future purchase.
   - Option to move items to the main cart or remove them.
   Total price for all items in the main cart.
   "Proceed to Checkout" button.
- **Process**
   - User navigates to the Cart Page from any part of the site.
   - The system retrieves all items from the `Cart_Items` table for the user.
   - Items are displayed in two sections: main cart and saved for later.
   - Users can update quantities, remove items, or move items between sections.
   - The page dynamically updates totals as changes are made.
   - When ready, the user can proceed to checkout.

#### **2. Detailed Order Page**:
- See purchases section 

#### **3. Checkout Page**:
- **Purpose**:Facilitates the process of converting `Cart_Items` into an `Order`.
- **Content**:
   - Review of all items in the cart with quantities and prices.
   - Total order amount.
   - User's current account balance.
   - Confirmation button to place the order.
- **Process**:
   - User navigates from the Cart Page to the Checkout Page.
   - The system displays all items from the user's cart `Cart_Items`.
   - The page shows the user's current balance for verification.
   - When the user confirms:
      - The system checks inventory availability and user's balance.
      - If successful, it creates a new entry in the Orders table.
      - Items are moved from `Cart_Items` to `Orders_Items`.
      - Product inventories and user/seller balances are updated.
      - The user is redirected to the Order Confirmation Page.

#### **4. Confirmation Page**:
- **Purpose**: Confirms successful placement of an order and provides order details.
- **Content**:
   - Confirmation message with order ID.
   - Summary of ordered items, quantities, and prices.
   - Total amount charged.
   - Expected fulfillment information.
   - Link to continue shopping or view order details.
- **Process**:
   This page is displayed immediately after a successful checkout.
   It retrieves and displays information from the newly created `Order` and `Orders_Items` entries.
   Provides the user with confirmation and next steps.

# REPORT.pdf – Inventory/Order Fulfillment (Sellers Guru)

## 1. Database Design

### Inventory Table
- **Purpose**: Store the quantity of all products left in the user’s inventory.
- **Columns**:
  - `user_id`: `INT`  
    - **Primary Key**, **Foreign Key** References `Users(user_id)`.  
    - Unique ID of the owner of the inventory.
  - `product_id`: `INT`  
    - **Primary Key**, **Foreign Key** References `Product(product_id)`.  
    - Unique ID of the product in the user’s inventory.
  - `quantity`: `INT`  
    - Available quantity for sale of the product in the inventory.
- **Restrictions**:
  - Key is given by `user_id` and `product_id` since each seller can only have one instance of a specific product in their inventory.

### History of Orders Table
- **Purpose**: Store orders for the specific seller.
- **Columns**:
  - `order_id`: `INT`  
    - **Primary Key**.  
    - Unique ID of the order from a user for a specific product submitted to the seller.
  - `date_order_placed`: `DATETIME`  
    - Date and time of the order submission.
  - `fulfilled`: `BOOL`  
    - Whether the product has been fulfilled by the seller or not.
- **Restrictions**:
  - Each line stores an order of one specific product submitted to the seller because each order can request multiple products.
  - Key is given by a new unique `order_id` because there can be many products in every order and products can be in multiple orders.

### Ordered Items Information Table
- **Purpose**: Store items from history of orders and their fulfillment status.
- **Columns**:
  - `order_id`: `INT`  
    - **Primary Key**, **Foreign Key** References `History_of_Orders(order_id)`.  
    - Unique ID of the order from a user for a specific product submitted to the seller.
  - `date_order_placed`: `DATETIME`  
    - Date and time of the order submission.
  - `fulfilled`: `BOOL`  
    - Whether the product has been fulfilled by the seller or not.
  - `buyer_id`: `INT`  
    - **Foreign Key** References `Orders(user_id)`.  
    - Unique ID of the buyer of the order.
  - `seller_id`: `INT`  
    - **Foreign Key** References `Users(user_id)`.  
    - Unique ID of the seller of the order.
  - `product_id`: `INT`  
    - **Foreign Key** References `Product(product_id)`.  
    - Unique ID of the product requested by the buyer.
  - `total_amount/number_of_items`: `INT`  
    - Quantity of the product requested by the buyer.
  - `buyer_address`: `VARCHAR(255)`  
    - The address of the buyer.

## 2. User Flows and Page-by-Page Design

### 1. Inventory Page
- **Purpose**: Allows sellers to view and manage items in their inventory.
- **Content**:
  - List of products left in seller’s inventory with product unique ID and available quantity for sale.
  - Options to add products or remove products.
- **Process**:
  - User navigates to the Inventory Page from any part of the site.
  - The system retrieves all items from the `Inventory` table for the user.
  - Items are displayed as a list.
  - Users can add products or remove products from the list.
  - The page dynamically updates totals as changes are made.
- **Possible Additional Features**:
  - Visualization/analytics of the inventory showing popularity and trends of products.

### 2. History of Order Page
- **Purpose**: Allows sellers to view and manage orders from their buyers.
- **Content**:
  - **Fulfilled Section**:
    - List of fulfilled orders sorted in reverse chronological order by default, including `order_id` and `date_order_placed`.
    - Options to mark an order as fulfilled or not fulfilled.
  - **Not Fulfilled Section**:
    - List of not fulfilled orders sorted in reverse chronological order by default, including `order_id`, `date_order_placed`.
    - Options to mark an order as fulfilled or not fulfilled.
- **Process**:
  - User navigates to the History of Order page from any part of the site.
  - The system displays all items from the user's `History_of_Orders` in fulfilled/not fulfilled sections.
  - Users can update the fulfillment status of orders. When the fulfillment status changes, the order is automatically placed in the other section.
  - Users can view order information by clicking on the `order_id`.
- **Possible Additional Features**:
  - Visualization/analytics to show the popularity and trends of the products.

### 3. Order Information Page
- **Purpose**: Allows sellers to view detailed information of each order.
- **Content**:
  - `buyer_id`
  - `buyer_address`
  - `date_order_placed`
  - `product_id`
  - `total_amount/number_of_items`
  - `fulfillment_status`
  - Options to mark an order as fulfilled or not.
- **Process**:
  - User navigates from the History of Order page to the Order Information page.
  - The system displays the information of the specific order.
  - Users can mark the order as fulfilled or not.
- **Possible Additional Features**:
  - Analytics about buyers who have worked with this seller, e.g., ratings, number of messages, etc.

## Implementation Status

### Core Features
1. **User Management** (Fully Functional)
   - Registration with email validation ✓
   - Login/logout with session management ✓
   - Profile editing ✓
   - Password change functionality ✓
   - Multiple address management ✓
   - Balance management with overdraft protection ✓
   - Real-time form validation ✓

2. **Product Management** (Fully Functional)
   - Product catalog ✓
   - Search functionality ✓
   - Filter system ✓
   - Product ranking ✓
   - Image handling ✓
   - Inventory tracking ✓

3. **Shopping Experience** (Fully Functional)
   - Shopping cart ✓
   - Wishlist ✓
   - Checkout process ✓
   - Order history ✓
   - Save for later ✓

4. **Seller Features** (Fully Functional)
   - Inventory management ✓
   - Order fulfillment ✓
   - Sales tracking ✓
   - Product listing ✓
   - Analytics dashboard ✓

5. **Social Features** (Fully Functional)
   - Product reviews ✓
   - User messaging ✓
   - Feedback system ✓
   - Social interactions ✓

### Security Implementation
1. **SQL Injection Prevention**
   - Parameterized queries throughout the application
   - Input validation and sanitization
   - Prepared statements for database operations

2. **Authentication & Authorization**
   - Session management
   - Password hashing with salt
   - CSRF protection
   - Role-based access control

3. **Data Validation**
   - Client-side validation
   - Server-side validation
   - Real-time feedback
   - Error handling

### Database Details
- **Size**: 
  - Users: 1,000
  - Products: 5,000
  - Purchases: 10,000
  - Orders: 8,000
  - Order Items: 15,000
  - Cart Items: 3,000
  - Wishes: 5,000
  - Feedback: 7,000
  - Inventory: 6,000
  - Addresses: 2,000
  - Balance Transactions: 5,000
- **Data Type**: 
  - Synthetic data generated using Faker library
  - Realistic patterns for user profiles and transactions
  - Generated product information with categories
  - Simulated purchase and order history
- **Generation**: Using `db/generated/gen.py` with configurable dataset sizes

### Hard-coded Values
1. **System Configuration**
   - Database connection parameters (in .flaskenv)
   - Password hashing algorithm (pbkdf2:sha256)
   - Default PostgreSQL port (5432)

2. **Business Rules**
   - Product categories (Electronics, Books, Clothing, Food, Home, Sports, Toys)
   - Transaction types (deposit/withdraw)
   - Order statuses (Pending/Fulfilled/Cancelled)
   - Default address flag (boolean)

3. **Data Constraints**
   - Email uniqueness
   - Product name uniqueness
   - Foreign key relationships
   - Default timestamps (UTC)
   - Price decimal precision (12,2)

## Technical Architecture
- **Backend**: Python Flask
- **Database**: PostgreSQL
- **Frontend**: HTML5, CSS3, JavaScript
- **Security**: Flask-Login, WTForms
- **UI Framework**: Bootstrap with custom GitHub-inspired styling

## Repository Structure
```
app/
├── models/          # Database models
├── templates/       # HTML templates
├── static/          # Static assets
├── routes.py        # Route handlers
└── forms.py         # Form definitions

db/
├── generated/       # Data generation scripts
├── create.sql      # Database schema
└── load.sql        # Initial data

tests/              # Test suite
docs/               # Documentation
```

## Testing Flow
1. **Guest User Testing**
   - Browse products
   - Search and filter
   - View details
   - Attempt restricted actions

2. **Authentication Testing**
   - Register
   - Login/logout
   - Profile management
   - Security checks

3. **Buyer Testing**
   - Cart operations
   - Checkout process
   - Purchase history
   - Balance management

4. **Seller Testing**
   - Inventory control
   - Order management
   - Sales tracking
   - Product updates

## Additional Features
1. **Enhanced UI/UX**
   - Real-time validation
   - Responsive design
   - Modern styling
   - Intuitive navigation

2. **Performance Optimizations**
   - Database indexing
   - Query optimization
   - Caching implementation
   - Lazy loading

3. **Extra Functionality**
   - Wishlist management
   - Save for later
   - Advanced search
   - Rich text product descriptions

## Known Issues
1. **Minor Bugs**
   - Search pagination on mobile devices
   - Image upload occasional timeout
   - Cart sync delay with slow connections

2. **Partial Implementations**
   - Advanced analytics dashboard
   - Bulk product upload
   - Social sharing features

## Future Improvements
1. **Planned Features**
   - Mobile app integration
   - Advanced analytics
   - AI-powered recommendations
   - Social media integration

2. **Technical Debt**
   - Code refactoring
   - Test coverage expansion
   - Documentation updates
   - Performance optimization

## Individual Scoring Preferences
All team members have agreed to team scoring. No individual scoring requested.

## Acknowledgments
- Course Staff for guidance
- Teaching Assistants for support
- Open Source Community for resources
- Fellow students for feedback

---