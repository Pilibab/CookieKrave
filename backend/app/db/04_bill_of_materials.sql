create table bom (
    bom_id serial primary key,
    prod_id int not null,
    inv_id int not null,
    bom_quan_req decimal(12, 3) not null, -- QUANTITY REQUIRED 

    -- Define the Foreign Key constraints
    constraint fk_product 
        foreign key (prod_id) 
        references products(prod_id),

    constraint fk_component 
        foreign key (inv_id) 
        references inventory (inv_id),

    constraint chk_quantity_required
    check (bom_quan_req > 0)
);