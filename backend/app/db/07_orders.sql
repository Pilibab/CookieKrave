create table orders (
    ord_id serial primary key,
    cust_id uuid not null,
    fulfillment_id int not null,
    ord_time timestamp default current_timestamp,
    -- total_amount decimal (7, 2) not null,        -- derived attr hence reducted 
    ord_pay_meth varchar(64),                       -- BOth payment and fullfillment method should be its own entity i think 
                                                    -- well see how it goes    

    ord_status varchar(25) default 'PENDING',
    ord_fulfillment_time timestamp,

    constraint chk_ord_status 
        check (ord_status in ('PENDING', 'DELIVERED')),

    constraint fk_customer_id
        foreign key (cust_id) 
        references customers(cust_id),

    constraint fk_fulfillment_id
        foreign key (fulfillment_id) 
        references fulfillment(fulfillment_id)
); 