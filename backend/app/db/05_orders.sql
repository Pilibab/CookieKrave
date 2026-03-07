CREATE TABLE ORDERS (
    order_id SERIAL PRIMARY KEY

    order_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_amount DECIMAL (7, 2) NOT NULL,
    payment_method VARCHAR(64),             -- BOth payment and fullfillment method should be its own entity i think 
    fullfillment_method VARCHAR(64)         -- well see how it goes 
); 