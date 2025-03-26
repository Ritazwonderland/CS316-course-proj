# Mini-Amazon Project - Final Submission
**Team Name**: Backlog Bashers  
**Course**: CS316 Fall 2024

## Submission Checklist
- [x] Demo Video (~10 minutes) - https://youtu.be/TpHdPpoZPCM
- [x] Project Report (REPORT.pdf)
- [x] Code (CODE.zip)
- [x] README_FINAL.md

## Video Submissions
1. **Main Demo Video (10 minutes)**
   - Complete walkthrough of all features
   - Testing flow demonstration
   - Error handling showcase
   - Link: https://youtu.be/TpHdPpoZPCM


## Team Members and Roles

1. **Juntang** - Users Guru (Account/Purchases)
   - **Core Features Implementation**
     - User authentication system with email validation
     - Profile management with real-time updates
     - Purchase history tracking and display
     - Balance management with overdraft protection
     - Address management system with multiple addresses
     - Wishlist functionality with real-time updates
   
   - **UI/UX Improvements**
     - Implemented GitHub-inspired modern design
     - Enhanced form validation with real-time feedback
     - Added responsive layouts for all user pages
     - Improved navigation and user flow
     - Created consistent styling across user features
     - Enhanced error messaging and user feedback
   
   - **AI Chatbot Integration**
     - Implemented AI-powered customer service chatbot
     - Added natural language processing for user queries
     - Created context-aware response system
     - Integrated with user account features
     - Added support for common user questions
     - Implemented real-time chat interface
     - Enhanced user support experience
     - Added intelligent query routing
   
   - **Database and Schema**
     - Designed user-related tables structure
     - Implemented foreign key constraints
     - Created balance transaction system
     - Added address management tables
     - Improved timestamp handling
     - Enhanced user balance tracking
   
   - **Data Generation and Management**
     - Implemented user data generation with realistic patterns
     - Generated balanced user account data
     - Created diverse purchase history patterns
     - Added address data generation with validation
     - Developed transaction history generation
   
   - **Performance Optimizations**
     - Optimized account dashboard for large datasets
     - Improved purchase history with pagination
     - Enhanced balance management features
     - Refined wishlist functionality performance
     - Added real-time form validation
   
   - **Security Enhancements**
     - Implemented password hashing and salting
     - Added CSRF protection
     - Created input validation and sanitization
     - Developed secure session management
     - Added real-time balance validation
   
   - **Documentation and Setup**
     - Wrote initial README.txt
     - Documented database structure
     - Created user management documentation
     - Added API endpoint documentation
     - Maintained feature documentation
   
   - **Files Maintained**:
     - `app/routes.py` (user-related routes)
     - `app/models/user.py`
     - `app/models/address.py`
     - `app/models/balance.py`
     - `app/models/wish.py`
     - `app/templates/account_dashboard.html`
     - `app/templates/edit_profile.html`
     - `app/templates/change_password.html`
     - `app/templates/add_address.html`
     - `app/templates/add_funds.html`
     - `app/templates/withdraw_funds.html`
   
   - **Final Enhancements**
     - Balance Management
       - Added real-time balance validation
       - Implemented overdraft protection
       - Enhanced transaction history tracking
       - Improved withdrawal limits enforcement
       - Added visual balance feedback
     - UI/UX Improvements
       - Implemented GitHub-inspired modern design
       - Added responsive layouts for all pages
       - Enhanced form validation with real-time feedback
       - Improved error messaging and user alerts
       - Created consistent styling across features
     - Performance Optimizations
       - Enhanced data generation with realistic patterns
       - Optimized dashboard for large datasets
       - Improved purchase history pagination
       - Added efficient query caching
       - Enhanced database indexing
     - Security Features
       - Strengthened input validation
       - Enhanced CSRF protection
       - Improved session management
       - Added secure transaction handling
     - Integration Features
       - Implemented AI chatbot support
       - Added context-aware responses
       - Enhanced user support experience
       - Integrated real-time chat interface
     
   Scoring Preference: Team scoring

2. **Lade** - Product Guru (Producks)
   - **Core Features Implementation**
      - Developed product catalog system
      - Implemented search and filter functionality
      - Created product ranking system
   - **Files Maintained**:
     - `app/search.py` 
     - `app/models/product.py`
     - `app/templates/product_page.html`
     - `app/templates/most_expensive.html`
   - **Final Enhancements**
      - Implement better user flow for product search
      - Added ratings and sellers for each product pages
      - Optimization product generation in gen.py  
   - Scoring Preference: Team scoring


3. **Chloe** - Cart Guru (Cart/Order)
   - **Core Features Implementation**
   - User shopping cart system
   - Implemented checkout process
   - Created order management
   - Added "save for later" feature
   - Developed cart synchronization (inventory and balance checking)
   - Implemented profile overview components related to orders
   - Scoring Preference: Team scoring
   - **Database and Schema**
   - Designed buyer related order tables structure
   - Implemented foreign key constraints
   - Created cart system
   - Added saved-for-later functionality
   - Enhanced inventory tracking for orders
   - Implemented a schema trigger for automatic updating order fulfillment
   - Fully integrated the orders/purchases across guru implementations
   - **Inventory and Balance for Carts/Orders**
   - Implemented inventory check to be able to add to cart
   - Checks balance and inventory before order can be submitted
   - Balance of seller and buyer is updated upon order
   - Inventory of seller is updated upon order
   - Low stock/balance prevents order

   - **Files Maintained**:
     - `app/cart_items.py` 
     - `app/orders.py`
     - `app/routes.py` (order related routes)
     - `app/index.py` (order related routes)
     - `app/models/cart_item.py`
     - `app/models/order_buy.py`
     - `app/models/order_item.py`
     - `app/models/order_items_Info.py` (fulfillment related methods)
     - `app/templates/cart.html`
     - `app/templates/checkout.html`
     - `app/templates/orders.html`
     - `app/templates/order_history.html` (page design and style)
     - `app/templates/feedback.html`
     - `app/templates/profile.html` (order related updates & recent activity)
     - `app/templates/index.html` (flash messages)

4. **Jiahe** - Seller Guru (Inventory/Order Fulfillment)
   - Created inventory management system
   - Implemented order fulfillment workflow
   - Built seller dashboard
   - Added order tracking functionality
   - Developed sales analytics
   - **Files Maintained**:
   - `app/inventory.py`
   - `app/models/inventory.py`
   - `app/models/ordered_Items_Info.py`
   - `app/order_history.py`
   - `app/templates/inventory.html`
   - `app/templates/order_history.html`
   - `app/templates/order_info.html`

   - Scoring Preference: Team scoring

5. **Alec** - Social Guru (Feedback/Messaging)
   - Implemented review system and ability to view reviews from user
   - Implemented fully-functional pagination for convenient access to large datasets of reviews
   - Ensured form data carried over into deeper pagination pages for convenience of user
   - Implemented ability to update or remove reviews for products and sellers
   - Added feedback social stats for customer viewing
   - Ensured smooth customer-side flow to access feedback page
   - Developed user interaction features
   - Improved UI for pleasant customer experience
   - Scoring Preference: Team scoring

---
© 2024 Backlog Bashers Team - CS316 Fall 2024