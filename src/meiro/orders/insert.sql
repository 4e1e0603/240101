-- delete from order_lines;
-- delete from products;
-- delete from orders;
-- delete from users;


insert into users (id, name, city) values (1, "user1", "city1");
insert into users (id, name, city) values (2, "user2", "city1");
insert into users (id, name, city) values (3, "user3", "city2");
insert into users (id, name, city) values (4, "user1", "city2");
insert into users (id, name, city) values (5, "name1", "city3");

insert into products(id, name, price) values (1, "product1", 1);
insert into products(id, name, price) values (2, "product2", 1);
insert into products(id, name, price) values (3, "product3", 1);
insert into products(id, name, price) values (4, "product4", 1);
insert into products(id, name, price) values (5, "product5", 1);

insert into orders (id, user_id) values (1, 1);

insert into order_lines(product_id, order_id) values (1, 1); 
insert into order_lines(product_id, order_id) values (2, 1); 
insert into order_lines(product_id, order_id) values (3, 1); 

select * from order_lines ol 
join products p on p.id = ol.product_id
join orders o on o.id = ol.order_id;

