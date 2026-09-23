-- ========================================================
-- ShopPulse Business Intelligence Queries
-- Business-driven questions & analytical SQL solutions
-- ========================================================

-- 1. What are the top 5 revenue-generating products in each category?
WITH ranked_products AS (
    SELECT 
        p.category,
        p.product_name,
        SUM(o.sales) AS total_revenue,
        SUM(o.profit) AS total_profit,
        DENSE_RANK() OVER (PARTITION BY p.category ORDER BY SUM(o.sales) DESC) AS rank
    FROM orders o
    JOIN products p ON o.product_id = p.product_id
    GROUP BY p.category, p.product_name
)
SELECT category, rank, product_name, total_revenue, total_profit
FROM ranked_products
WHERE rank <= 5
ORDER BY category, rank;

-- 2. Which sales channels have the highest cart/order abandonment rates?
SELECT 
    sales_channel,
    COUNT(*) AS total_orders,
    SUM(CASE WHEN order_status = 'Cancelled' THEN 1 ELSE 0 END) AS cancelled_orders,
    ROUND((SUM(CASE WHEN order_status = 'Cancelled' THEN 1 ELSE 0 END)::DECIMAL / COUNT(*)) * 100, 2) AS cancellation_rate_pct
FROM orders
GROUP BY sales_channel
ORDER BY cancellation_rate_pct DESC;

-- 3. Customer Lifetime Value (CLV) analysis by customer segment
SELECT 
    c.customer_segment,
    COUNT(DISTINCT c.customer_id) AS customer_count,
    SUM(o.sales) AS total_revenue,
    AVG(o.sales) AS avg_order_value,
    ROUND(SUM(o.sales) / COUNT(DISTINCT c.customer_id), 2) AS avg_clv
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_segment
ORDER BY avg_clv DESC;

-- 4. Discount Impact Analysis — Does higher discount lead to higher sales or negative profit?
SELECT 
    CASE 
        WHEN discount = 0 THEN 'No Discount (0%)'
        WHEN discount <= 0.10 THEN 'Low (1-10%)'
        WHEN discount <= 0.25 THEN 'Medium (11-25%)'
        ELSE 'High (>25%)'
    END AS discount_tier,
    COUNT(order_line_id) AS item_count,
    SUM(sales) AS total_sales,
    SUM(profit) AS total_profit,
    ROUND((SUM(profit) / NULLIF(SUM(sales), 0)) * 100, 2) AS margin_pct
FROM orders
GROUP BY 1
ORDER BY total_sales DESC;
