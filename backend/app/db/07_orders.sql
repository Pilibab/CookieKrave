
CREATE TYPE payment_method_enum AS ENUM ('Cash', 'GCash');
CREATE TYPE order_status_enum AS ENUM (
    'Pending', 
    'Preparing', 
    'Out for Delivery', 
    'Completed', 
    'Cancelled'
);

CREATE TABLE orders (
    ord_id SERIAL PRIMARY KEY,
    cust_id UUID NOT NULL,
    fulfillment_id INT NOT NULL,
    ord_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ord_fulfillment_time TIMESTAMP,
    
    -- Using the unified ENUM columns cleanly with defaults
    payment_method payment_method_enum NOT NULL DEFAULT 'Cash',
    order_status order_status_enum NOT NULL DEFAULT 'Pending',

    -- Foreign Key Constraints
    CONSTRAINT fk_customer_id
        FOREIGN KEY (cust_id) 
        REFERENCES customers(cust_id),

    CONSTRAINT fk_fulfillment_id
        FOREIGN KEY (fulfillment_id) 
        REFERENCES fulfillment(fulfillment_id)
);