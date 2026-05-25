-- Drop the type if it already exists (and cascade it to clear dependent columns if re-running)
drop type if exists unit_type cascade;

-- Now create it cleanly without the invalid syntax
create type unit_type as enum ('pcs', 'ml', 'g', 'kg');

create table inventory (
    inv_id serial primary key,
    inv_ing_name varchar(64) not null,
    inv_stock decimal(10,3) not null default 0.0,
    inv_uom unit_type not null, 
    inv_rt decimal(10,2) not null default 0,

    constraint chk_current_stock check (inv_stock >= 0),
    constraint chk_reorder_trigger check (inv_rt >= 0)
);