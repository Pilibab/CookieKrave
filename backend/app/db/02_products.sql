create table products (
    prod_id int primary key,
    prod_name varchar(64) not null,
    prod_desc varchar(255) not null,
    prod_price decimal (7, 2) not null, -- till xxxxx.xx
    prod_available boolean default true,
    prod_sl date not null,               -- SHELF LIFE 
    prod_image_url varchar(512) default 'https://ghhowjijwfgffcbjlsxl.supabase.co/storage/v1/object/public/product_img/default_no_img.png',
constraint chk_prod_price
check (prod_price >= 0)
);