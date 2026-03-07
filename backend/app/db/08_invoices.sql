CREATE TABLE INVOICES (
    invoice_id SERIAL PRIMARY KEY,
    order_id int NOT NULL,

    invoice_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,   -- The specific time the bill was made
    bill_detail VARCHAR(255),                           -- should be its own class ig 
    CONSTRAINT FK_order_id 
        FOREIGN KEY (order_id) 
        REFERENCES ORDERS(order_id),
);