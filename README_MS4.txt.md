<!-- # Owned by Backlog Bashers as part of course project for CS316 2024FALL
# Drafted by Juntang at Oct 30, 2024  -->

# README_MS4.txt

**Team Name**: Backlog Bashers

## Team Members and Roles:
1. **Juntang**: Users Guru (Account/Purchases)
2. **Lade**: Product Guru (Producks)
3. **Chloe**: Cart Guru (Cart/Order)
4. **Jiahe**: Seller Guru (Inventory/Order Fulfillment)
5. **Alec**: Social Guru (Feedback/Messaging)

## Summary of Progress:

After MS3, we have been working on implementing the advanced features for Milestone 4. Including but not limited to:
- Large database generation

## Large Database Generation
The code for generating our large test database can be found in:
- `db/generate/gen.py`: Main data generation script
- `db/generate/data/`: Generated CSV files
- `db/setup.sh generated`: Script to load the generated data

To generate and load the large database:
```bash
cd db/generate
python gen.py
cd ../..
./db/setup.sh generated
```
### **Juntang (Users Guru)**:
- Enhanced Data Generation and Management:
  - Implemented user data generation with realistic patterns
  - Generated balanced user account data with varying balances
  - Created diverse purchase history patterns
  - Added address data generation with proper validation

- Schema and Database Improvements:
  - Resolved conflicts in Wishes table structure
  - Added proper foreign key constraints for user-related tables
  - Improved timestamp handling for user activities
  - Enhanced user balance tracking

- User Management Features:
  - Optimized account dashboard performance for large datasets
  - Improved purchase history display with pagination
  - Enhanced balance management features with transaction history
  - Refined wishlist functionality with better performance

- Recent Improvements:
  - Enhanced User Interface and Experience:
    - Redesigned user profile page with modern dashboard layout
    - Integrated all user-related functionalities into a single, intuitive interface
    - Added tabbed navigation for better organization of user features
    - Improved address management system with visual feedback
    - Enhanced balance management with better visual presentation

  - Profile Features:
    - Dashboard overview with key metrics (total orders, spending, cart items)
    - Recent activity tracking with detailed transaction history
    - Improved address management with default address handling
    - Enhanced security settings with password management
    - Streamlined balance management with top-up and withdrawal features

  - Technical Improvements:
    - Optimized database queries for better performance
    - Enhanced error handling and user feedback
    - Improved form validation and submission handling
    - Added proper transaction handling for critical operations
    - Fixed address management bugs and improved default address logic

The implementation can be found in:
- Backend:
  - `db/generated/gen.py`: User data generation
  - `app/models/user.py`: Optimized user queries
  - `app/models/balance.py`: Enhanced balance tracking
  - `app/models/wish.py`: Improved wishlist handling
  - `app/routes.py`: Enhanced user routes with better organization
  - `app/models/address.py`: Improved address management logic
  - `db/generated/gen.py`: Enhanced address generation with proper defaults
- Frontend:
  - `app/templates/account_dashboard.html`: Updated UI for large datasets
  - `app/templates/purchase_history.html`: Added pagination
  - `app/templates/profile.html`: New comprehensive user dashboard
  - `app/templates/edit_address.html`: Improved address editing interface
  - `app/templates/base.html`: Enhanced navigation and layout

### **Lade (Product Guru)**:
- Search Page:
  - Completed search page with category and name search
  - Added page to view product
  - added backend to add and update products
The implementation can be found in:
- Backend:
  - `app/k-expensive.py`
  - `app/add_product.py`
  - `app/models/product.py`

- Frontend:
  - `app/templates/add_product.html`
  - `app/templates/product_page.html`
  - `app/templates/update_product.html`
  - `app/templates/most-expensive.html`


### **Chloe (Cart Guru)**:
- User Interface
  - Updated Cart Page to match the style of the main and profile pages
  - Updated Checkout Page to match the style of the main and profile pages
  - Updated Order History Page to match the style of the main and profile pages
- Profile features
  - Connected the overview section to update numbers based on the real-time contents of a user’s cart
  - Connected the overview section to update numbers based on the real-time orders and spending of a user
  - The Cart Items and Total Orders sections of the overview section can be clicked on to go to the cart and the orders pages respectively

The implementation can be found in:
- Backend:
  - `app/routes.py`: Integrated routes to find the number of orders, items in cart, and total amount spent
  - `app/models/order_buy.py`: Added routes to find the total number of orders and total amount spent
  - `app/models/cart_item.py`: Added route to find the count of items in the cart
- Frontend:
  - `app/templates/profile.html`: Buttons for respective pages and active counting display
  - `app/templates/cart.html`: Improved design and appearence
  - `app/templates/checkout.html`: Improved design and appearence
  - `app/templates/orders.html`: Improved design and appearence
  - `app/templates/order_history.html`: Improved design and appearence

### **Jiahe (Seller Guru)**:
- User interface
  - Updated inventory page to match the style and design of other pages, changed the add/remove button for better user experience
  - Updated order history and order info page to match the style and design of other pages
- Profile features
  - Updated inventory and order history page so that they show corresponding items directly for the user landing the page
  - Improved add/remove function to modify the existing products in the inventory at a flexible quantity

The implementation can be found in:
- Backend:
  - `app/inventory.py`
  - `app/models/inventory.py`
  - `app/models/ordered_Items_Info.py`
- Frontend:
  - `app/templates/inventory.html`
  - `app/templates/order_history.html`
  - `app/templates/order_info.html`

### **Alec (Social Guru)**:
- Feedback Improvement:
  - Support for large datasets has been added
  - Pagination has been added for user feedback listings

The implementation can be found in:
- Backend:
  - `app/feedback.py`
  - `app/models/modelFeedback.py`
- Frontend:
  - `app/templates/feedback.html`


## Demo Video:
Our team's demo video showcasing all implemented APIs and frontend widgets can be found at: [Insert video link here]

## Repository Link:
[Mini-Amazon CS 316 Project on GitLab](https://gitlab.oit.duke.edu/ool4/mini-amazon-cs-316-project)

## Implementation Details:

## Demo Video
Our MS4 demo video showcasing the working prototype can be found at: https://youtu.be/Bc8_5KkcA_Q

## Advanced Features Implementation
[TBD]