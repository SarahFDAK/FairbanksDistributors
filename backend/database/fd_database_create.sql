create table chains
(
    chain_id   serial primary key,
    chain_name varchar(30) unique not null
    -- potentially add in billing info and other stuff relevant to customers
);

create table categories
(
    category_id   serial primary key,
    category_name varchar(30) unique not null,
    type          varchar(10)        not null -- Ex: chips, bread, taco_loco
);

create table stores
(
    store_id    serial primary key,
    store_name  varchar(30) unique not null,
    customer_id serial             not null references chains (chain_id) match simple on update cascade on delete no action
);

create table orders
(
    order_id      serial primary key,
    store_id      serial not null references stores (store_id) match simple on update no action on delete no action,
    order_date    date   not null,
    delivery_date date   not null,
    notes         text
);

create table items
(
    item_id       serial primary key,
    item_name     varchar(30) not null, -- Note: This has not been made unique
    category      varchar(30) not null references categories (category_name) match simple on update no action on delete no action,
    ounces        float(2),
    pack_quantity smallint,
    upc           varchar(8),
    is_active     bool
);

create table promos
(
    item_id     serial        not null references items (item_id) match simple on update no action on delete no action,
    customer_id serial        not null references chains (chain_id) match simple on update no action on delete no action,
    price       numeric(4, 2) not null, -- assumes no item costs more than $99.99
    start_date  date          not null,
    end_date    date          not null, -- Need to consider off by one with these dates
    primary key (item_id, customer_id)
);

create table ordered_items
(
    order_id      serial   not null references orders (order_id) match simple on update no action on delete no action,
    item_id       serial   not null references items (item_id) match simple on update no action on delete no action,
    qty_ordered   smallint not null,
    qty_delivered smallint,
    primary key (order_id, item_id)
);
