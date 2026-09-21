CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    city VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    category VARCHAR(100),
    price NUMERIC(10, 2) NOT NULL,
    stock INTEGER DEFAULT 0
);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(id),
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(30) NOT NULL,
    total_amount NUMERIC(10, 2) NOT NULL
);

CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES orders(id),
    product_id INTEGER NOT NULL REFERENCES products(id),
    quantity INTEGER NOT NULL,
    unit_price NUMERIC(10, 2) NOT NULL
);

INSERT INTO customers (name, email, city) VALUES
('Aarav Sharma', 'aarav@example.com', 'Pune'),
('Priya Patil', 'priya@example.com', 'Mumbai'),
('Rahul Joshi', 'rahul@example.com', 'Pune'),
('Sneha Kulkarni', 'sneha@example.com', 'Nashik'),
('Amit Deshmukh', 'amit@example.com', 'Nagpur');

INSERT INTO products (name, category, price, stock) VALUES
('Laptop', 'Electronics', 65000.00, 20),
('Mouse', 'Electronics', 1200.00, 100),
('Keyboard', 'Electronics', 2500.00, 50),
('Headphones', 'Audio', 3500.00, 40),
('Monitor', 'Electronics', 18000.00, 15);

INSERT INTO orders (customer_id, status, total_amount) VALUES
(1, 'completed', 66200.00),
(2, 'completed', 3500.00),
(3, 'completed', 20500.00),
(1, 'cancelled', 1200.00),
(4, 'completed', 18000.00),
(5, 'pending', 2500.00),
(2, 'completed', 65000.00);

INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
(1, 1, 1, 65000.00),
(1, 2, 1, 1200.00),
(2, 4, 1, 3500.00),
(3, 5, 1, 18000.00),
(3, 2, 2, 1200.00),
(4, 2, 1, 1200.00),
(5, 5, 1, 18000.00),
(6, 3, 1, 2500.00),
(7, 1, 1, 65000.00);