---

# Owned by Backlog Bashers as part of course project for CS316 2024FALL
# Drafted by Juntang at Sep 22, 2024 

---

# README.txt

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

At this point, our team has focused on setting up the project infrastructure and preparing the necessary documentation to move forward with development. Here's a breakdown of what each team member has completed since the last milestone:

### **Lade (Product Guru)**:
- **GitLab Repository Setup**: Lade set up the GitLab repository and ensured that it is accessible to all team members for collaboration.
- Ensured the skeleton code was properly integrated into the repository and running in their local development environment.
-  Code for Product guru part of MS3 can be found in the following files: __init__.py, products.py, k_expensive.py ,k_expensive.html, create.sql, load.sql, and product_copy from the /data folder.  
### **Juntang (Users Guru)**:
- **README.txt Setup**: Juntang wrote the initial README.txt, detailing team roles, project selection, and progress so far.
- Set up the skeleton code in their local development environment.
- Contributed to the initial **REPORT.pdf** by defining the database structure for user-related tables, including user accounts, purchase history, and constraints for unique emails and user IDs.
- The implementation can be found in:`app/routes.py`, `app/models/user.py`, `app/models/address.py`, app/models/balance.py`,`app/models/wish.py`, `app/templates/account_dashboard.html`, `app/templates/edit_profile.html`, `app/templates/change_password.html`, `app/templates/add_address.html`, `app/templates/add_funds.html`, `app/templates/withdraw_funds.html`


### **Alec (Social Guru)**:
- Set up skeleton code in local environment and contributed to the documentation of the feedback and messaging system in the **REPORT.pdf**.
- Code for social guru part of MS3 can be found in the following files: __init__.py, feedback.py, feedback.html, modelFeedback.py, create.sql, load.sql, and data from the /data folder.
  
### **Chloe (Cart Guru)**:
- Set up the skeleton code in their local environment and contributed to the README and **REPORT.pdf** for cart functionality, detailing how users can add products to the cart, modify quantities, and submit orders.
- Defined the database structure for cart and order related tables and pages, ensuring the inclusion of a save for later feature
- The functionality can by found in the models "cart_item", "order_item", and "order_buy"; The templates "cart", "order_items", "orders" and "checkout"; the blueprints "cart_items", "order_items", and "orders".
- The specific functionality for MS3 is in "cart_item.py", "cart_items.py", and "cart.html".

### **Jiahe (Seller Guru)**:
- Set up skeleton code in local environment and contributed to the documentation of the inventory and order fulfillment in the **REPORT.pdf**.
- Contributed to the seller-related sections of the **REPORT.pdf**, defining the database structure for inventory and order fulfillment including inventory table, history of order table, and order information table.
- Code for sellers guru part of MS3 can be found in: app/__init__.py; app/inventory.py; app/models/inventory.py; app/models/ordered_Items_Info.py; app/order_history.py; app/templates/inventory.html; app/templates/order_history.html; app/templates/order_info.html; db/load.sql

## Repository Link:
[Mini-Amazon CS 316 Project on GitLab](https://gitlab.oit.duke.edu/ool4/mini-amazon-cs-316-project)

## MS4 Generated Data Program Location:
db/generated/gen.py

## MS4 Demo Video Link:
https://youtu.be/Bc8_5KkcA_Q
