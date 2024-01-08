drop table if exists users;
----
drop table if exists orders;
----
drop table if exists products;
----
drop table if exists products_orders;
----
create table users (
  id integer primary key not null,
  name text not null check(name <> ''), 
  city text not null  
);
----
create table products (
  id integer primary key not null,  
  name text not null check(name <> ''), 
  price integer not null check(price >= 0)  
);
----
create table orders (
  id integer primary key not null,
  user_id integer not null, 
  foreign key(user_id) references users(id)
);
----
create table products_orders (
    order_id integer not null,
    product_id integer not null,    
    foreign key(order_id) references orders(id),
    foreign key(product_id) references products(id),
    unique(order_id, product_id) 
    -- todo quantity per order
);