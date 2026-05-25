CREATE TABLE "PRODUCTS" (
    "PROD_ID" INT PRIMARY KEY,
    "PROD_NAME" VARCHAR(64) NOT NULL,
    "PROD_DESC" VARCHAR(255) NOT NULL,
    "PROD_PRICE" DECIMAL (7, 2) NOT NULL, -- till xxxxx.xx
    "PROD_AVAILABLE" BOOLEAN DEFAULT true,
    "PROD_SL" DATE NOT NULL               -- SHELF LIFE 
    "PROD_IMAGE_URL" VARCHAR(512) DEFAULT 'https://ghhowjijwfgffcbjlsxl.supabase.co/storage/v1/object/public/product_img/default_no_img.png';
CONSTRAINT chk_PROD_PRICE
CHECK (PROD_PRICE >= 0)
);