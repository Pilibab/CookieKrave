CREATE TABLE PRODUCTS (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(64) NOT NULL,
    product_desc VARCHAR(255) NOT NULL,
    price DECIMAL (7, 2) NOT NULL, -- till xxxxx.xx
    is_available BOOLEAN DEFAULT true,
    shelf_life DATE NOT NULL

CONSTRAINT chk_PRODUCT_PRICE
CHECK (price >= 0)
);