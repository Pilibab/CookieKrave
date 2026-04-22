CREATE TABLE ORDERS (
    ORD_ID SERIAL PRIMARY KEY,
    CUST_ID int NOT NULL,
    ORD_TIME TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    -- total_amount DECIMAL (7, 2) NOT NULL,        -- derived attr hence reducted 
    ORD_PAY_METH VARCHAR(64),                       -- BOth payment and fullfillment method should be its own entity i think 
                                                    -- well see how it goes    
    ORD_F_TYPE VARCHAR(64),                         -- fullfillment type             

    CONSTRAINT FK_customer_id
        FOREIGN KEY (CUST_ID) 
        REFERENCES CUSTOMERS(CUST_ID)
); 