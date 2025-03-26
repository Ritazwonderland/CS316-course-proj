\COPY Users FROM 'Users.csv' WITH DELIMITER ',' NULL '' CSV
-- since id is auto-generated; we need the next command to adjust the counter
-- for auto-generation so next INSERT will not clash with ids loaded above:
SELECT pg_catalog.setval('public.users_id_seq',
                         (SELECT MAX(id)+1 FROM Users),
                         false);

\COPY Products FROM 'Products.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.products_id_seq',
                         (SELECT MAX(id)+1 FROM Products),
                         false);

\COPY Purchases FROM 'Purchases.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.purchases_id_seq',
                         (SELECT MAX(id)+1 FROM Purchases),
                         false);

\COPY Wishes FROM 'Wishes.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.wishes_id_seq',
                         (SELECT MAX(id)+1 FROM Wishes),
                         false);

\COPY Ordered_Items_Info FROM 'Ordered_Items_Info.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.ordered_items_info_id_seq',
                         (SELECT MAX(id)+1 FROM Ordered_Items_Info),
                         false);

\COPY Inventory(user_id, product_id, quantity) FROM 'Inventory.csv' WITH DELIMITER ',' NULL '' CSV;

\COPY Feedback FROM 'Feedback.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.feedback_id_seq',
                         (SELECT MAX(id)+1 FROM Feedback),
                         false);

\COPY Orders FROM 'Orders.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.orders_id_seq',
                         (SELECT MAX(id)+1 FROM Orders),
                         false);

\COPY Order_Items(order_id, product_id, quantity, fulfilled, fulfillment_date, unit_price) FROM 'Order_Items.csv' WITH DELIMITER ',' NULL '' CSV;

\COPY Cart_Items FROM 'Cart_Items.csv' WITH DELIMITER ',' NULL '' CSV;

\COPY Addresses FROM 'Addresses.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.addresses_id_seq',
                         (SELECT MAX(id)+1 FROM Addresses),
                         false);

\COPY BalanceTransactions FROM 'BalanceTransactions.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.balancetransactions_id_seq',
                         (SELECT MAX(id)+1 FROM BalanceTransactions),
                         false);

\COPY Orders_Buy FROM 'Orders_Buy.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.orders_buy_order_id_seq',
                         (SELECT MAX(order_id)+1 FROM Orders_Buy),
                         false);