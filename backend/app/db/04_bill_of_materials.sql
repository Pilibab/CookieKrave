CREATE TABLE BOM (
    bom_id SERIAL PRIMARY KEY,
    product_id INT NOT NULL,
    inventory_id INT NOT NULL,
    quantity_required DECIMAL(12, 3) NOT NULL,

    -- Define the Foreign Key constraints
    CONSTRAINT fk_product 
        FOREIGN KEY (product_id) 
        REFERENCES PRODUCT(product_id),

    CONSTRAINT fk_component 
        FOREIGN KEY (inventory_id) 
        REFERENCES INVENTORY (inventory_id)
);