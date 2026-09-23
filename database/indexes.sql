-- ========================================================
-- ShopPulse Database Performance Optimization Indexes
-- ========================================================

-- Foreign Key & Join Indexes
CREATE INDEX idx_orders_customer_id ON orders(customer_id);
CREATE INDEX idx_orders_product_id ON orders(product_id);
CREATE INDEX idx_orders_order_date ON orders(order_date);
CREATE INDEX idx_orders_order_status ON orders(order_status);
CREATE INDEX idx_orders_sales_channel ON orders(sales_channel);

-- Analytical Filtering Indexes
CREATE INDEX idx_products_category ON products(category);
CREATE INDEX idx_products_sub_category ON products(sub_category);
CREATE INDEX idx_customers_state ON customers(state);
CREATE INDEX idx_customers_segment ON customers(customer_segment);

-- Composite Index for Revenue Analytics
CREATE INDEX idx_orders_date_status_sales ON orders(order_date, order_status, sales);
