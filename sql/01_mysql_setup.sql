-- ============================================================
-- MySQL setup for the Amazon Sales project (MySQL Workbench)
-- Run this first, then import the CSV, then run 02_analysis_queries.sql
-- ============================================================

CREATE DATABASE IF NOT EXISTS amazon_sales;
USE amazon_sales;

DROP TABLE IF EXISTS sales;

CREATE TABLE sales (
    Order_ID        VARCHAR(9)     PRIMARY KEY,
    Order_Date      DATE,
    Year            INT,
    Month           INT,
    Month_Name      VARCHAR(3),
    Quarter         INT,
    Customer_ID     VARCHAR(10),
    Category        VARCHAR(40),
    Product_Name    VARCHAR(40),
    Region          VARCHAR(10),
    City            VARCHAR(20),
    Unit_Price      DECIMAL(10,2),
    Quantity        INT,
    `Discount_%`    DECIMAL(5,2),
    Discount_Amount DECIMAL(12,2),
    Gross_Revenue   DECIMAL(12,2),
    Net_Revenue     DECIMAL(12,2),
    Payment_Mode    VARCHAR(20),
    Order_Status    VARCHAR(12),
    Is_Completed    VARCHAR(5),
    Rating          DECIMAL(3,1)
);

-- ------------------------------------------------------------
-- Load the cleaned CSV. Choose ONE of these two options.
--
-- Option A (MySQL Workbench wizard, no code):
--   In the left panel, right-click the table "sales" under
--   amazon_sales > Tables > "Table Data Import Wizard",
--   pick data/amazon_sales_clean.csv, choose "Use existing table: sales",
--   keep the column mapping, and click Next until it finishes.
--
-- Option B (code, replace the path with your own):
--   Needs local_infile enabled:  SET GLOBAL local_infile = 1;
-- ------------------------------------------------------------
-- LOAD DATA LOCAL INFILE 'C:/Amazon_data_Analysis/data/amazon_sales_clean.csv'
-- INTO TABLE sales
-- FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
-- LINES TERMINATED BY '\n'
-- IGNORE 1 LINES;

-- Check the load. Expected: 10486 rows
SELECT COUNT(*) AS rows_loaded FROM sales;
