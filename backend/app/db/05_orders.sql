CREATE TABLE ORDERS (
    order_id SERIAL PRIMARY KEY,
    customer_id int NOT NULL,
    order_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_amount DECIMAL (7, 2) NOT NULL,
    payment_method VARCHAR(64),             -- BOth payment and fullfillment method should be its own entity i think 
    fullfillment_method VARCHAR(64)         -- well see how it goes 

    CONSTRAINT FK_customer_id
        FOREIGN KEY (customer_id) 
        REFERENCES CUSTOMERS(customer_id),
); 