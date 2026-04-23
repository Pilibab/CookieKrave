-- 1. Create the custom type first
CREATE TYPE unit_type AS ENUM ('pcs', 'ml', 'g', 'kg');

-- 2. Then create the table that uses it
CREATE TABLE INVENTORY (
    INV_ID SERIAL PRIMARY KEY,
    INV_ING_NAME VARCHAR(64) NOT NULL,
    INV_STOCK DECIMAL(10,3) NOT NULL DEFAULT 0.0,
    INV_UOM unit_type NOT NULL, -- Now the DB knows what 'unit_type' is
    INV_RT DECIMAL(10,2) NOT NULL DEFAULT 0,

    CONSTRAINT chk_current_stock CHECK (INV_STOCK >= 0),
    CONSTRAINT chk_reorder_trigger CHECK (INV_RT >= 0)
);