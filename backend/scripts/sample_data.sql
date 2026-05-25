-- Populate customers [cite: 12]
insert into customers (cust_firstname, cust_lastname, cust_middlename, cust_email, cust_social_provider, cust_cont_no)
values 
('Alice', 'Guo', 'V', 'alice.guo@email.com', 'google',  '+639123456789'),
('Bob', 'Reyes', 'A', 'bob.reyes@email.com', 'facebook',  '+639987654321');

-- Populate products [cite: 13]
insert into products (prod_id, prod_name, prod_desc, prod_price, prod_available, prod_sl)
values 
(101, 'Classic Choco Chip', 'Soft-baked cookie with dark chocolate chips', 45.00, true, '2026-05-10'),
(102, 'Red Velvet Cream', 'Red velvet cookie with cream cheese filling', 55.00, true, '2026-05-08');

-- Populate riders [cite: 22]
insert into rider (rider_id, rider_name, rider_contact_num)
values 
(1, 'John Doe', '+639111222333');

-- Populate fulfillment types [cite: 23]
-- This table defines the categories used by Delivery and Pick_Up
insert into fulfillment (fulfillment_type)
values 
('Delivery'),
('Pick_Up');

-- Populate inventory [cite: 15]
-- Uses the unit_type enum: 'pcs', 'ml', 'g', 'kg' [cite: 14]
insert into inventory (inv_ing_name, inv_stock, inv_uom, inv_rt)
values 
('All-Purpose Flour', 50.000, 'kg', 5.00),
('Dark Chocolate Chips', 20.000, 'kg', 2.00),
('Cream Cheese', 10.000, 'kg', 1.00);

-- Populate bom (Bill of Materials) [cite: 16]
-- Links products to inventory
insert into bom (prod_id, inv_id, bom_quan_req)
values 
(101, 1, 0.250), -- 250g flour for Choco Chip
(101, 2, 0.100), -- 100g chocolate for Choco Chip
(102, 3, 0.150); -- 150g cream cheese for Red Velvet

-- Populate orders [cite: 18]
-- Depends on customers [cite: 20]
insert into orders (cust_id, ord_pay_meth, ord_f_type)
values 
(1, 'GCash', 'Delivery'),
(2, 'Cash', 'Pick_Up');

-- Populate cart [cite: 21]
-- Links orders to products
insert into cart (ord_id, prod_id, cart_quan)
values 
(1, 101, 2), -- Alice ordered 2 Choco Chip cookies
(1, 102, 1), -- Alice ordered 1 Red Velvet cookie
(2, 101, 5); -- Bob ordered 5 Choco Chip cookies

-- Populate delivery details [cite: 24]
-- Depends on fulfillment (ID 1) and rider (ID 1)
insert into delivery (fulfillment_id, rider_id, address, contact_name, contact_number, note)
values 
(1, 1, '123 Rizal St, Legazpi City', 'Alice Guo', '+639123456789', 'Near the blue gate');

-- Populate pick_up details [cite: 25]
-- Depends on fulfillment (ID 2)
insert into pick_up (fulfillment_id, preferred_time, pick_up_location)
values 
(2, '2026-04-24 14:00:00', 'CookieKrave Main Branch - Daraga');

-- Populate invoices [cite: 26]
-- Linked to the orders
insert into invoices (ord_id, invoice_dets)
values 
(1, 'Total: PHP 145.00 - Paid via GCash'),
(2, 'Total: PHP 225.00 - Pending Cash Payment');