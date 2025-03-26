<!-- # Owned by Backlog Bashers as part of course project for CS316 2024FALL
# Drafted by Juntang at Oct 20, 2024  -->

---

# README_MS3.txt

**Team Name**: Backlog Bashers

## Team Members and Roles:
1. **Juntang**: Users Guru (Account/Purchases)
2. **Lade**: Product Guru (Producks)
3. **Chloe**: Cart Guru (Cart/Order)
4. **Jiahe**: Seller Guru (Inventory/Order Fulfillment)
5. **Alec**: Social Guru (Feedback/Messaging)

## Project Option:
We have chosen the **standard project option**.

## Summary of Progress:

Our team has successfully implemented the required backend API endpoints and frontend widgets for Milestone 3. Here's a breakdown of what each team member has completed:

### **Juntang (Users Guru)**:
- Implemented the backend API endpoint to find all purchases of a given user id.
- Created the frontend widget to display and interact with the purchase history results.
- Implemented user profile management features:
  - Edit profile information (name, email)
  - Change password functionality
  - Add and manage multiple addresses
- Implemented balance management features:
  - View current balance
  - Add funds to account
  - Withdraw funds from account
- Created wishlist functionality:
  - Add products to wishlist
  - Remove products from wishlist
  - View wishlist
- The implementation can be found in:
  - Backend: 
    - `app/routes.py` (functions: `get_user_purchases`, `account_dashboard`, `edit_profile`, `change_password`, `add_address`, `add_funds`, `withdraw_funds`)
    - `app/models/user.py`
    - `app/models/address.py`
    - `app/models/balance.py`
    - `app/models/wish.py`
  - Frontend: 
    - `app/templates/account_dashboard.html`
    - `app/templates/edit_profile.html`
    - `app/templates/change_password.html`
    - `app/templates/add_address.html`
    - `app/templates/add_funds.html`
    - `app/templates/withdraw_funds.html`

### **Lade (Product Guru)**:
- [Lade to fill in details about their implementation]

### **Chloe (Cart Guru)**:
- [Chloe to fill in details about their implementation]

### **Jiahe (Seller Guru)**:
- [Jiahe to fill in details about their implementation]

### **Alec (Social Guru)**:
- [Alec to fill in details about their implementation]

## Demo Video:
Our team's demo video showcasing all implemented APIs and frontend widgets can be found at: [Insert video link here]

## Repository Link:
[Mini-Amazon CS 316 Project on GitLab](https://gitlab.oit.duke.edu/ool4/mini-amazon-cs-316-project)

## Implementation Details:
- The Users Guru's implementation for finding all purchases of a given user id can be found in:
  - Backend API: `app/routes.py` (function: `get_user_purchases`)
  - Frontend Widget: `app/templates/account_dashboard.html` (Purchase History section)
  - Database Query: `app/models/purchase.py` (method: `get_user_purchases_with_summary`)

- The admin page for searching user purchases is implemented in:
  - Backend: `app/routes.py` (function: `admin`)
  - Frontend: `app/templates/admin.html`

- User profile management features:
  - Edit profile: `app/routes.py` (function: `edit_profile`), `app/templates/edit_profile.html`
  - Change password: `app/routes.py` (function: `change_password`), `app/templates/change_password.html`
  - Address management: `app/routes.py` (functions: `add_address`, `set_default_address`, `delete_address`), `app/templates/add_address.html`

- Balance management features:
  - Add funds: `app/routes.py` (function: `add_funds`), `app/templates/add_funds.html`
  - Withdraw funds: `app/routes.py` (function: `withdraw_funds`), `app/templates/withdraw_funds.html`

- Wishlist functionality:
  - Backend: `app/models/wish.py`
  - Frontend: Integrated into `app/templates/account_dashboard.html`

These implementations allow for comprehensive user account management, including searching user purchases, displaying the results, managing personal information, addresses, account balance, and wishlist functionality.
