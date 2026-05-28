create table customers (
    cust_id uuid primary key, 
    cust_firstname varchar(50) not null, 
    cust_lastname varchar(50) not null, 
    cust_middlename varchar(50), 
    cust_email varchar(255) unique not null,
    cust_social_provider varchar(50), -- 'google' | 'facebook'
    cust_cont_no varchar(20),          -- contact number 
    cust_cd timestamp default current_timestamp -- THIS IS CREATE DATE 
);