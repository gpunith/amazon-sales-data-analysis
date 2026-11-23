-- ============================================================
-- Amazon Sales SQL analysis (MySQL 8+)
-- Run after 01_mysql_setup.sql. Table: sales
-- ============================================================
USE amazon_sales;

-- Query 01: Overall KPIs
SELECT
    COUNT(DISTINCT Order_ID)                              AS total_orders,
    COUNT(DISTINCT Customer_ID)                           AS unique_customers,
    SUM(Quantity)                                         AS units_sold,
    ROUND(SUM(Gross_Revenue), 2)                          AS gross_revenue,
    ROUND(SUM(Discount_Amount), 2)                        AS total_discount,
    ROUND(SUM(Net_Revenue), 2)                            AS net_revenue,
    ROUND(SUM(Net_Revenue) / COUNT(DISTINCT Order_ID), 2) AS avg_order_value,
    ROUND(AVG(Rating), 2)                                 AS avg_rating,
    ROUND(100.0 * SUM(Order_Status = 'Delivered') / COUNT(*), 1) AS completion_rate_pct
FROM sales;

-- Query 02: Revenue by category
SELECT
    Category,
    COUNT(*)                                  AS orders,
    SUM(Quantity)                             AS units_sold,
    ROUND(SUM(Net_Revenue), 2)                AS net_revenue,
    ROUND(100.0 * SUM(Net_Revenue) / (SELECT SUM(Net_Revenue) FROM sales), 1) AS pct_of_revenue,
    ROUND(AVG(Rating), 2)                     AS avg_rating
FROM sales
GROUP BY Category
ORDER BY net_revenue DESC;

-- Query 03: Revenue by region
SELECT
    Region,
    COUNT(*)                                  AS orders,
    ROUND(SUM(Net_Revenue), 2)                AS net_revenue,
    ROUND(SUM(Net_Revenue) / COUNT(*), 2)     AS avg_order_value
FROM sales
GROUP BY Region
ORDER BY net_revenue DESC;

-- Query 04: Monthly revenue trend
SELECT
    Year,
    Month,
    Month_Name,
    COUNT(*)                                  AS orders,
    ROUND(SUM(Net_Revenue), 2)                AS net_revenue
FROM sales
GROUP BY Year, Month, Month_Name
ORDER BY Year, Month;

-- Query 05: Top 10 products by revenue
SELECT
    Product_Name,
    Category,
    SUM(Quantity)                             AS units_sold,
    ROUND(SUM(Net_Revenue), 2)                AS net_revenue,
    ROUND(AVG(Rating), 2)                     AS avg_rating
FROM sales
GROUP BY Product_Name, Category
ORDER BY net_revenue DESC
LIMIT 10;

-- Query 06: Payment mode share
SELECT
    Payment_Mode,
    COUNT(*)                                  AS orders,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM sales), 1) AS pct_of_orders,
    ROUND(SUM(Net_Revenue), 2)                AS net_revenue
FROM sales
GROUP BY Payment_Mode
ORDER BY orders DESC;

-- Query 07: Order status breakdown
SELECT
    Order_Status,
    COUNT(*)                                  AS orders,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM sales), 1) AS pct_of_orders,
    ROUND(SUM(Net_Revenue), 2)                AS revenue_impacted
FROM sales
GROUP BY Order_Status
ORDER BY orders DESC;

-- Query 08: Discount band effectiveness
SELECT
    CASE
        WHEN `Discount_%` = 0   THEN '0% (No Discount)'
        WHEN `Discount_%` <= 10 THEN '1-10%'
        WHEN `Discount_%` <= 20 THEN '11-20%'
        ELSE '21%+'
    END                                       AS discount_band,
    COUNT(*)                                  AS orders,
    SUM(Quantity)                             AS units_sold,
    ROUND(SUM(Quantity) / COUNT(*), 2)        AS avg_units_per_order,
    ROUND(SUM(Net_Revenue), 2)                AS net_revenue
FROM sales
GROUP BY discount_band
ORDER BY MIN(`Discount_%`);

-- Query 09: One-time vs repeat customers
WITH customer_orders AS (
    SELECT Customer_ID, COUNT(*) AS order_count, SUM(Net_Revenue) AS revenue
    FROM sales
    GROUP BY Customer_ID
)
SELECT
    CASE WHEN order_count = 1 THEN 'One-time' ELSE 'Repeat' END AS customer_type,
    COUNT(*)                                  AS customers,
    ROUND(SUM(revenue), 2)                    AS total_revenue,
    ROUND(SUM(revenue) / COUNT(*), 2)         AS revenue_per_customer
FROM customer_orders
GROUP BY customer_type;

-- Query 10: Quarterly revenue
SELECT
    Year,
    Quarter,
    COUNT(*)                                  AS orders,
    ROUND(SUM(Net_Revenue), 2)                AS net_revenue
FROM sales
GROUP BY Year, Quarter
ORDER BY Year, Quarter;

-- Query 11: Average rating and return rate by category
SELECT
    Category,
    ROUND(AVG(Rating), 2)                                         AS avg_rating,
    ROUND(100.0 * SUM(Order_Status = 'Returned')  / COUNT(*), 1)  AS return_rate_pct,
    ROUND(100.0 * SUM(Order_Status = 'Cancelled') / COUNT(*), 1)  AS cancel_rate_pct
FROM sales
GROUP BY Category
ORDER BY return_rate_pct DESC;

-- Query 12: Top 5 cities by revenue
SELECT
    City,
    Region,
    COUNT(*)                                  AS orders,
    ROUND(SUM(Net_Revenue), 2)                AS net_revenue
FROM sales
WHERE City <> 'Unknown'
GROUP BY City, Region
ORDER BY net_revenue DESC
LIMIT 5;
