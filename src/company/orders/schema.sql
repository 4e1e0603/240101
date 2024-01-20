--
-- A database schema for ordering service.
--

CREATE TABLE IF NOT EXISTS version (
    major INT,
    minor INT,
    patch INT,
    --
    CONSTRAINT check_major CHECK (major >= 0),
    CONSTRAINT check_minor CHECK (minor >= 0),
    CONSTRAINT check_patch CHECK (patch >= 0),
    CONSTRAINT check_version CHECK (
        major >= 0
        OR minor >= 0
        OR patch >= 0
    )
);

INSERT INTO VERSION (major, minor, patch) VALUES (0, 1, 0);

-- The users of our application placing the orders. 
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY key NOT NULL,
    name text NOT NULL CHECK(name <> ''),
    city text NOT NULL CHECK(name <> '')
);

-- The products ordered by our users.
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY key NOT NULL,
    name text NOT NULL CHECK(name <> ''),
    price INTEGER NOT NULL CHECK(price >= 0)
);

-- The orders purchased by our users.
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY key NOT NULL,
    user_id INTEGER NOT NULL,
    created TIMESTAMP(10) NOT NULL,
    CONSTRAINT fk_users FOREIGN key(user_id) REFERENCES users(id)
);

-- The order line connects a product with order.
CREATE TABLE IF NOT EXISTS order_lines (
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 1,
    CONSTRAINT fk_orders FOREIGN key(order_id) REFERENCES orders(id) ON DELETE cascade,
    CONSTRAINT fk_products FOREIGN key(product_id) REFERENCES products(id) ON DELETE cascade
    CONSTRAINT pk_order_lines PRIMARY KEY (order_id, product_id)
);