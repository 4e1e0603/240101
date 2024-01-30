--
-- A database schema for ordering service.
--

-- The schema's semantic version.
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
    id INTEGER PRIMARY KEY NOT NULL,
    name text NOT NULL CHECK(name <> ''),
    city text NOT NULL CHECK(name <> '')
);

-- The products purchased by customers.
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY NOT NULL,
    name text NOT NULL CHECK(name <> ''),
    price INTEGER NOT NULL CHECK(price >= 0)
);

-- The orders with products created by customers.
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY NOT NULL,
    user_id INTEGER NOT NULL,
    created TIMESTAMP(10) NOT NULL,
    CONSTRAINT fk_users FOREIGN KEY(user_id) REFERENCES users(id)
);

-- The order line connects a product with order.
CREATE TABLE IF NOT EXISTS order_lines (
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 1,
    CONSTRAINT fk_orders FOREIGN KEY(order_id) REFERENCES orders(id) ON DELETE CASCADE,
    CONSTRAINT fk_products FOREIGN KEY(product_id) REFERENCES products(id) ON DELETE CASCADE,
    CONSTRAINT pk_order_lines PRIMARY KEY (order_id, product_id)
);
