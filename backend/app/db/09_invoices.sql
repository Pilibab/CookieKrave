CREATE TABLE INVOICES (
    ORD_ID int NOT NULL,

    INVOICE_DATE TIMESTAMP DEFAULT CURRENT_TIMESTAMP,   -- The specific time the bill was made
    INVOICE_DETS VARCHAR(255),                          -- should be its own class ig, INVOICE DETAIL
    CONSTRAINT FK_order_id 
        FOREIGN KEY (ORD_ID) 
        REFERENCES ORDERS(ORD_ID)
);