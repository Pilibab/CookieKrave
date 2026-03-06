CREATE TABLE CUSTOMER (
    customer_id SERIAL PRIMARY KEY, 
    full_name VARCHAR(255), 
    email VARCHAR(255) UNIQUE NOT NULL,
    social_provider VARCHAR(50), -- 'google' | 'facebook'
    social_id VARCHAR(255) UNIQUE, -- from sign-on
    contact_number VARCHAR(20) NOT NULL, -- dont use int or decimal for number 
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);