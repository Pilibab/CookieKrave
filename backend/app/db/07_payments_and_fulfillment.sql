create TABLE DELIEVERY (
    order_id INT PRIMARY KEY REFERENCES ORDERS(order_id),


);

CREATE TABLE PICK_UP (
    order_id INT PRIMARY KEY REFERENCES ORDERS(order_id),
    preferred_time TIMESTAMP,
    pick_up_location VARCHAR(255)   -- move this as a seperate entity so that we can reuse the adress 
);