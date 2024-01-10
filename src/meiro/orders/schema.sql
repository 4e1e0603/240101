--
-- A database schema for ordering service.
--
-- Statements are delimited by four dashes so it can be 
-- splited and feeded to `cursor.execute()` one by one.
--

----
create table if not exists version (
  major int,
  minor int,
  patch int,
  --
  constraint check_major check (major >= 0),
  constraint check_minor check (minor >= 0),
  constraint check_patch check (patch >= 0),
  constraint check_version check (
    major >= 0
    or minor >= 0
    or patch >= 0
  )
);

-- Table comments are not suported so we add our comments to custom table.

----
create table if not exists table_comments (
  table_name text,
  table_comment text,
  constraint pk_table_comments primary key (table_name, table_comment) 
);

----
insert into table_comments (table_name, table_comment) values ("users", "The users of our application");
----
create table if not exists users (
  id integer primary key not null,
  name text not null check(name <> ''),
  city text not null
);

----
insert into table_comments (table_name, table_comment) values ("products", "The products ordered by our users");
----
create table if not exists products (
  id integer primary key not null,
  name text not null check(name <> ''),
  price integer not null check(price >= 0)
);


----
insert into table_comments (table_name, table_comment) values ("orders", "The orders purchased by our users.")
----
create table if not exists orders (
  id integer primary key not null,
  user_id integer not null,
  constraint fk_users foreign key(user_id) references users(id)
);

----
insert into table_comments (table_name, table_comment) values ("order_lines", "The order line connects a product with order.")
----
create table if not exists order_lines (
  order_id integer not null,
  product_id integer not null,
  constraint fk_orders foreign key(order_id) references orders(id) on delete cascade,
  constraint fk_products foreign key(product_id) references products(id) on delete cascade,
  constraint pk_order_lines primary key (order_id, product_id) 
  -- todo quantity per order
);


