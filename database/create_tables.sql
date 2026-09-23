-- ========================================================
-- ShopPulse E-Commerce Database Schema DDL
-- Compatible with PostgreSQL, MySQL, and SQLite
-- ========================================================

-- Drop tables if exists (clean setup)
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS region;
DROP TABLE IF EXISTS payments;

-- 1. Customers Table
CREATE TABLE customers (
    customer_id VARCHAR(50) PRIMARY KEY,
    customer_name VARCHAR(150) NOT NULL,
    gender VARCHAR(20),
    age INT,
    city VARCHAR(100),
    state VARCHAR(100),
    country VARCHAR(100),
    customer_segment VARCHAR(50),
    signup_date DATE
);

-- 2. Products Table
CREATE TABLE products (
    product_id VARCHAR(50) PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    category VARCHAR(100) NOT NULL,
    sub_category VARCHAR(100),
    brand VARCHAR(100),
    cost DECIMAL(12, 2),
    list_price DECIMAL(12, 2)
);

-- 3. Region Table
CREATE TABLE region (
    region_id VARCHAR(50) PRIMARY KEY,
    country VARCHAR(100),
    state VARCHAR(100),
    city VARCHAR(100),
    region_name VARCHAR(100)
);

-- 4. Payments Table
CREATE TABLE payments (
    payment_id VARCHAR(50) PRIMARY KEY,
    payment_method VARCHAR(50) NOT NULL
);

-- 5. Orders Fact Table
CREATE TABLE orders (
    order_id VARCHAR(50) NOT NULL,
    order_line_id VARCHAR(50) PRIMARY KEY,
    order_date TIMESTAMP NOT NULL,
    ship_date TIMESTAMP,
    customer_id VARCHAR(50) REFERENCES customers(customer_id),
    product_id VARCHAR(50) REFERENCES products(product_id),
    quantity INT NOT NULL,
    unit_price DECIMAL(12, 2) NOT NULL,
    discount DECIMAL(5, 2) DEFAULT 0.00,
    sales DECIMAL(12, 2) NOT NULL,
    cost DECIMAL(12, 2) NOT NULL,
    profit DECIMAL(12, 2) NOT NULL,
    shipping_cost DECIMAL(10, 2) DEFAULT 0.00,
    payment_method VARCHAR(50),
    order_status VARCHAR(50) DEFAULT 'Completed',
    sales_channel VARCHAR(50) DEFAULT 'Direct'
);
