-- ========================================================
-- ShopPulse Core Analytical SQL Queries
-- ========================================================

-- 1. Executive Monthly Revenue & Profit Trends
SELECT 
    DATE_TRUNC('month', o.order_date) AS month,
    COUNT(DISTINCT o.order_id) AS total_orders,
    SUM(o.sales) AS total_revenue,
    SUM(o.profit) AS total_profit,
    ROUND((SUM(o.profit) / NULLIF(SUM(o.sales), 0)) * 100, 2) AS profit_margin_pct
FROM orders o
WHERE o.order_status NOT IN ('Cancelled')
GROUP BY 1
ORDER BY 1 ASC;

-- 2. Category Performance Summary
SELECT 
    p.category,
    COUNT(DISTINCT o.order_id) AS order_count,
    SUM(o.quantity) AS units_sold,
    SUM(o.sales) AS category_revenue,
    SUM(o.profit) AS category_profit,
    ROUND(SUM(o.sales) * 100.0 / SUM(SUM(o.sales)) OVER (), 2) AS revenue_share_pct
FROM orders o
JOIN products p ON o.product_id = p.product_id
GROUP BY p.category
ORDER BY category_revenue DESC;

-- 3. Top 10 States by Sales & Margin
SELECT 
    c.state,
    COUNT(DISTINCT c.customer_id) AS total_customers,
    COUNT(DISTINCT o.order_id) AS total_orders,
    SUM(o.sales) AS state_revenue,
    SUM(o.profit) AS state_profit,
    ROUND((SUM(o.profit) / NULLIF(SUM(o.sales), 0)) * 100, 2) AS profit_margin_pct
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
GROUP BY c.state
ORDER BY state_revenue DESC
LIMIT 10;

-- 4. Customer RFM Base View
WITH customer_orders AS (
    SELECT 
        customer_id,
        MAX(order_date) AS last_order_date,
        COUNT(DISTINCT order_id) AS frequency,
        SUM(sales) AS monetary
    FROM orders
    GROUP BY customer_id
)
SELECT 
    customer_id,
    CURRENT_DATE - last_order_date::date AS recency_days,
    frequency,
    monetary
FROM customer_orders;
