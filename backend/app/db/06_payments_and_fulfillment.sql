create table fulfillment (
    fulfillment_id serial primary key,
    fulfillment_type varchar(50) not null,
constraint chk_fulfillment_type 
check (fulfillment_type in ('Delivery', 'Pick_Up')));

create table delivery (
    fulfillment_id int not null,
    rider_id int not null,
    address varchar(255) not null,
    contact_name varchar(100) null,
    contact_number varchar(20) null,
    note varchar(500) null,
    floor_unit_num varchar(50) null,
constraint delivery_pk primary key (fulfillment_id),
constraint delivery_fulfillment_fk foreign key (fulfillment_id) references fulfillment(fulfillment_id),
constraint delivery_rider_fk foreign key (rider_id) references rider(rider_id));

create table pick_up (
    fulfillment_id int not null,
    preferred_time timestamp null, -- Changed DATETIME to TIMESTAMP
    pick_up_location varchar(255) null,
constraint pickup_pk primary key (fulfillment_id),
constraint pickup_fulfillment_fk foreign key (fulfillment_id) references fulfillment(fulfillment_id));

