CREATE TABLE INVENTORY (
    inventory_id SERIAL PRIMARY KEY,
    ingredient_name VARCHAR(64) NOT NULL,
    current_stock DECIMAL(10,3) NOT NULL DEFAULT 0.0,
    unit_of_measure VARCHAR(10) NOT NULL,               -- 'g', 'ml', 'pcs', etc.
    reorder_trigger DECIMAL(10,2) NOT NULL DEFAULT 0,   -- reorder when the amt is met

CONSTRAINT chk_current_stock
CHECK (current_stock >= 0),
CONSTRAINT chk_reorder_trigger
CHECK (reorder_trigger >= 0)
);