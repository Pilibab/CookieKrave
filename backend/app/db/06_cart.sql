CREATE TABLE CART (
    order_id int NOT NULL,
    product_id int NOT NULL,
    quantity int DEFAULT 1,
    price_per_item DECIMAL (7, 2) NOT NULL,
    CONSTRAINT FK_order_id
        FOREIGN KEY (order_id) 
        REFERENCES ORDERS(order_id),
    CONSTRAINT FK_product_id
        FOREIGN KEY (product_id) 
        REFERENCES PRODUCTS(product_id),
);