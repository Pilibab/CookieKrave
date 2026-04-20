CREATE TABLE INVENTORY (
    INV_ID SERIAL PRIMARY KEY,
    INV_ING_NAME VARCHAR(64) NOT NULL,
    INV_STOCK DECIMAL(10,3) NOT NULL DEFAULT 0.0,
    INV_UOM VARCHAR(10) NOT NULL,               -- 'g', 'ml', 'pcs', etc.
    INV_RT DECIMAL(10,2) NOT NULL DEFAULT 0,    -- RT (reorder trigger) reorder when the amt is met

CONSTRAINT chk_current_stock
CHECK (INV_STOCK >= 0),
CONSTRAINT chk_reorder_trigger
CHECK (INV_RT >= 0)
);