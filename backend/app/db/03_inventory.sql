CREATE TABLE INVENTORY (
    inventory_id SERIAL PRIMARY KEY,
    name VARCHAR(64),
    current_stock DECIMAL(10,3) DEFAULT 0.000,
    unit_of_measure VARCHAR(10) NOT NULL, -- 'g', 'ml', 'pcs', etc.
    reorder_trigger INT
);