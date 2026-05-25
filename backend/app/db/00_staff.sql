create table staff (
    staff_id uuid primary key,
    staff_name varchar(64) not null,
    staff_email varchar(255) unique not null,
    role varchar(20) default 'admin' not null, -- Defaults to admin automatically!
    
    constraint chk_staff_role check (role in ('admin', 'manager', 'baker'))
);