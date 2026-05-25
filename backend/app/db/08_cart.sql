create table cart (
    ord_id int not null,
    prod_id int not null,
    cart_quan int default 1,
    constraint fk_order_id
        foreign key (ord_id) 
        references orders(ord_id),
    constraint fk_product_id
        foreign key (prod_id) 
        references products(prod_id)
);