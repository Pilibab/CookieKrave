-- Populate CUSTOMERS [cite: 12]
INSERT INTO CUSTOMERS (CUST_FIRSTNAME, CUST_LASTNAME, CUST_MIDDLENAME, CUST_EMAIL, CUST_SOCIAL_PROVIDER, CUST_SOCIALID, CUST_CONT_NO)
VALUES 
('Alice', 'Guo', 'V', 'alice.guo@email.com', 'google', 'google_12345', '+639123456789'),
('Bob', 'Reyes', 'A', 'bob.reyes@email.com', 'facebook', 'fb_67890', '+639987654321');

-- Populate PRODUCTS [cite: 13]
INSERT INTO PRODUCTS (PROD_ID, PROD_NAME, PROD_DESC, PROD_PRICE, PROD_AVAILABLE, PROD_SL)
VALUES 
(101, 'Classic Choco Chip', 'Soft-baked cookie with dark chocolate chips', 45.00, true, '2026-05-10'),
(102, 'Red Velvet Cream', 'Red velvet cookie with cream cheese filling', 55.00, true, '2026-05-08');

-- Populate RIDERS [cite: 22]
INSERT INTO RIDER (RIDER_ID, RIDER_NAME, RIDER_CONTACT_NUM, CURRENT_LOCATION)
VALUES 
(1, 'John Doe', '+639111222333', 'Legazpi City Center');

-- Populate FULFILLMENT TYPES [cite: 23]
-- This table defines the categories used by Delivery and Pick_Up
INSERT INTO FULFILLMENT (FULFILLMENT_TYPE)
VALUES 
('Delivery'),
('Pick_Up');

-- Populate INVENTORY [cite: 15]
-- Uses the unit_type ENUM: 'pcs', 'ml', 'g', 'kg' [cite: 14]
INSERT INTO INVENTORY (INV_ING_NAME, INV_STOCK, INV_UOM, INV_RT)
VALUES 
('All-Purpose Flour', 50.000, 'kg', 5.00),
('Dark Chocolate Chips', 20.000, 'kg', 2.00),
('Cream Cheese', 10.000, 'kg', 1.00);

-- Populate BOM (Bill of Materials) [cite: 16]
-- Links PRODUCTS to INVENTORY
INSERT INTO BOM (PROD_ID, INV_ID, BOM_QUAN_REQ)
VALUES 
(101, 1, 0.250), -- 250g flour for Choco Chip
(101, 2, 0.100), -- 100g chocolate for Choco Chip
(102, 3, 0.150); -- 150g cream cheese for Red Velvet

-- Populate ORDERS [cite: 18]
-- Depends on CUSTOMERS [cite: 20]
INSERT INTO ORDERS (CUST_ID, ORD_PAY_METH, ORD_F_TYPE)
VALUES 
(1, 'GCash', 'Delivery'),
(2, 'Cash', 'Pick_Up');

-- Populate CART [cite: 21]
-- Links ORDERS to PRODUCTS
INSERT INTO CART (ORD_ID, PROD_ID, CART_QUAN)
VALUES 
(1, 101, 2), -- Alice ordered 2 Choco Chip cookies
(1, 102, 1), -- Alice ordered 1 Red Velvet cookie
(2, 101, 5); -- Bob ordered 5 Choco Chip cookies

-- Populate DELIVERY details [cite: 24]
-- Depends on FULFILLMENT (ID 1) and RIDER (ID 1)
INSERT INTO DELIVERY (FULFILLMENT_ID, RIDER_ID, ADDRESS, CONTACT_NAME, CONTACT_NUMBER, NOTE)
VALUES 
(1, 1, '123 Rizal St, Legazpi City', 'Alice Guo', '+639123456789', 'Near the blue gate');

-- Populate PICK_UP details [cite: 25]
-- Depends on FULFILLMENT (ID 2)
INSERT INTO PICK_UP (FULFILLMENT_ID, PREFERRED_TIME, PICK_UP_LOCATION)
VALUES 
(2, '2026-04-24 14:00:00', 'CookieKrave Main Branch - Daraga');

-- Populate INVOICES [cite: 26]
-- Linked to the ORDERS
INSERT INTO INVOICES (ORD_ID, INVOICE_DETS)
VALUES 
(1, 'Total: PHP 145.00 - Paid via GCash'),
(2, 'Total: PHP 225.00 - Pending Cash Payment');