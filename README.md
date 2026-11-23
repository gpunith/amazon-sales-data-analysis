# Amazon Sales Data Analysis

An end-to-end data analytics project using **Python, MySQL, Excel, and Power BI**. This project demonstrates how raw sales data can be cleaned, analysed, and transformed into meaningful business insights through SQL queries and interactive dashboards.

> **Dataset Disclaimer:** This project uses a synthetic e-commerce sales dataset generated using Python for portfolio and learning purposes. It does not contain actual Amazon sales or customer data and is not affiliated with Amazon.

## 1. Project Introduction

Businesses generate large amounts of sales data every day. Analysing this data helps organisations understand sales performance, customer behaviour, product trends, and business opportunities.

The objective of this project is to simulate a real-world Data Analyst workflow using an e-commerce sales dataset. The project starts with raw, inconsistent data and transforms it into a clean dataset for analysis and dashboard reporting.

### Project Objectives

- Generate a raw sales dataset containing realistic data-quality issues.
- Clean and transform data using Python and Pandas.
- Store and analyse the cleaned data using MySQL.
- Perform sales analysis using SQL queries.
- Create an Excel dashboard with summary reports and visualizations.
- Build an interactive Power BI dashboard.
- Identify important business insights from sales performance.

## 2. Tools and Technologies

| Technology | Purpose |
|---|---|
| Python | Data generation and processing |
| Pandas | Data cleaning and transformation |
| NumPy | Numerical operations and data generation |
| MySQL | Data storage and SQL analysis |
| MySQL Workbench | Executing SQL queries |
| Microsoft Excel | Data analysis and dashboard creation |
| OpenPyXL | Excel workbook automation |
| Matplotlib | Data visualization |
| Power BI | Interactive dashboard development |
| DAX | Power BI calculations and KPIs |

## 3. Project Workflow

```text
       Raw Sales Dataset
          10,750 Rows
               |
               v
       Python Data Cleaning
          (Pandas)
               |
               v
       Cleaned Dataset
          10,486 Rows
               |
       +-------+-------+
       |               |
       v               v
   MySQL Analysis   Excel Dashboard
       |               |
       v               v
   12 SQL Queries   KPI Cards & Charts
       |               |
       +-------+-------+
               |
               v
        Power BI Dashboard
               |
               v
        Business Insights
```

## 4. Dataset Information

The project uses a synthetic e-commerce sales dataset generated through Python.

### Dataset Files

| File | Description |
|---|---|
| `amazon_sales_raw.csv` | Original raw dataset with duplicates, missing values, inconsistent formats, and invalid records. |
| `amazon_sales_clean.csv` | Cleaned dataset prepared using Python and Pandas. |
| `amazon_sales_for_excel.csv` | Excel-ready dataset with additional calculated columns. |

### Dataset Size

| Description | Records |
|---|---:|
| Raw dataset | 10,750 |
| Cleaned dataset | 10,486 |
| Records removed during cleaning | 264 |

The cleaned dataset contains **21 columns**, including order details, customer information, product categories, revenue, discounts, payment methods, order status, and customer ratings.

### Main Dataset Columns

| Column | Description |
|---|---|
| `Order_ID` | Unique order identifier |
| `Order_Date` | Order date |
| `Year` | Order year |
| `Month` | Month number |
| `Month_Name` | Month name |
| `Quarter` | Financial/calendar quarter |
| `Customer_ID` | Customer identifier |
| `Category` | Product category |
| `Product_Name` | Product name |
| `Region` | Sales region |
| `City` | Customer city |
| `Unit_Price` | Price per unit |
| `Quantity` | Number of units ordered |
| `Discount_%` | Discount percentage |
| `Discount_Amount` | Discount amount |
| `Gross_Revenue` | Revenue before discount |
| `Net_Revenue` | Revenue after discount |
| `Payment_Mode` | Payment method |
| `Order_Status` | Order status |
| `Is_Completed` | Completion indicator |
| `Rating` | Customer rating |

## 5. Data Cleaning Using Python

The raw dataset contains intentional data-quality issues to demonstrate practical data-cleaning techniques.

### Cleaning Operations

- Identified and removed duplicate order records.
- Handled missing values.
- Standardised category, region, and city names.
- Replaced missing city and payment-mode values with `Unknown`.
- Parsed multiple date formats.
- Handled missing discount values.
- Filled missing ratings using the category median.
- Removed records with invalid dates, non-positive quantities, or non-positive unit prices.
- Calculated gross revenue, discount amount, and net revenue.
- Created year, month, month name, and quarter columns.
- Checked order ID uniqueness.

### Cleaning Results

| Metric | Result |
|---|---:|
| Raw rows | 10,750 |
| Cleaned rows | 10,486 |
| Duplicate order IDs after cleaning | 0 |
| Missing values after cleaning | 0 |

Missing city and payment information is retained as the text value `Unknown`, rather than as a blank or NULL value.

## 6. Key Results

The analysis produces the following overall sales metrics:

| KPI | Result |
|---|---:|
| Net Revenue | ₹2.65 Crore |
| Total Orders | 10,486 |
| Average Order Value | ₹2,526 |
| Unique Buyers | 2,893 |
| Cities Covered | 15 |
| Average Rating | 4.08 / 5 |
| Delivered Orders | 57.4% |
| Returned Orders | 14.0% |
| Cancelled Orders | 14.5% |
| Pending Orders | 14.1% |

*Values are rounded for presentation. Refer to the cleaned dataset and final dashboards for detailed figures.*

### Key Business Insights

**1. Order Fulfilment**

Only 57.4% of orders are delivered. This highlights an opportunity to improve delivery and order fulfilment performance.

**2. Returns and Cancellations**

Returned and cancelled orders together account for approximately 28.5% of orders. Understanding the reasons behind these orders could help reduce losses and improve customer satisfaction.

**3. Product Category Performance**

Revenue analysis helps identify the highest-performing product categories and categories that may need improvement.

**4. Regional Performance**

City and region analysis helps identify major sales-contributing locations and geographic opportunities.

**5. Customer Behaviour**

Customer-level analysis helps distinguish one-time buyers from repeat buyers and understand purchasing patterns.

**6. Payment Preferences**

Payment-mode analysis helps identify the commonly used payment methods and understand transaction preferences.

## 7. Dashboard Overview

### Excel Dashboard

The Excel dashboard includes:

- KPI cards.
- Category-wise sales analysis.
- Region-wise revenue analysis.
- Monthly sales trends.
- Customer segmentation.
- Payment and order-status summaries.
- City revenue analysis and map.

Excel workbook:

`outputs/Amazon_Sales_Dashboard.xlsx`

### Power BI Dashboard

The interactive Power BI dashboard includes:

- Net revenue and total orders.
- Average order value.
- Completion rate.
- Order status breakdown.
- Monthly order and revenue trends.
- Category performance.
- Category revenue by quarter.
- Payment-mode analysis.
- City-level revenue map.

Power BI file:

`powerbi/main_dashboard_amazon1.pbix`

### Python Visualizations

Matplotlib is used to create charts for:

- Monthly revenue trends.
- Category revenue.
- Regional revenue.
- Top-selling products.
- Payment-mode distribution.
- Order-status distribution.
- Rating and discount analysis.
- City-level performance.
- Other sales comparisons.

Generated charts are saved in:

`outputs/visualizations/`

### Dashboard Screenshot

![Amazon Sales Dashboard Overview](d:\amazon_new\scripts\sales_dashboard.png)

<img width="2040" height="2652" alt="sales_dashboard" src="https://github.com/user-attachments/assets/951f3b46-340d-483c-ba94-aa6d09607255" />

## 8. Folder Structure

```text
Amazon_data_Analysis/
│
├── README.md
├── requirements.txt
├── .gitignore
│
├── data/
│   ├── amazon_sales_raw.csv
│   ├── amazon_sales_clean.csv
│   └── amazon_sales_for_excel.csv
│
├── sql/
│   ├── 01_mysql_setup.sql
│   └── 02_analysis_queries.sql
│
├── scripts/
│   ├── 01_generate_raw_data.py
│   ├── 02_clean_data.py
│   ├── 03_prepare_excel_data.py
│   ├── 04_build_excel.py
│   ├── 05_dashboard_sheet.py
│   └── 06_visualizations.py
│
├── outputs/
│   ├── Amazon_Sales_Dashboard.xlsx
│   ├── india_city_map.png
│   └── visualizations/
│       └── Generated PNG charts
│
├── powerbi/
│   └── main_dashboard_amazon1.pbix
│
└── screenshots/
    └── dashboard_overview.png
```

## 9. How to Run the Project

Run all commands from the project's root folder.

### Step 1: Python Setup

Install Python and create a virtual environment.

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**

```bash
python -m venv venv
source venv/bin/activate
```

Install the required libraries:

```bash
pip install -r requirements.txt
```

### Step 2: Generate and Clean the Dataset

Run:

```bash
python scripts/01_generate_raw_data.py
python scripts/02_clean_data.py
```

The first script generates the raw synthetic dataset. The second script cleans and transforms the data.

The cleaned output is saved as:

`data/amazon_sales_clean.csv`

### Step 3: MySQL Database Setup and Analysis

1. Open MySQL Workbench.
2. Open `sql/01_mysql_setup.sql`.
3. Run the SQL script to create the `amazon_sales` database and `sales` table.
4. Import `data/amazon_sales_clean.csv` into the `sales` table using the Table Data Import Wizard, or follow the `LOAD DATA` instructions in the setup SQL file.
5. Open `sql/02_analysis_queries.sql`.
6. Execute the 12 SQL analysis queries.

### Step 4: Generate the Excel Dashboard

Close the Excel workbook before executing the scripts.

Run:

```bash
python scripts/03_prepare_excel_data.py
python scripts/04_build_excel.py
python scripts/05_dashboard_sheet.py
python scripts/06_visualizations.py
```

The scripts generate the Excel workbook and Matplotlib visualizations.

Excel output:

`outputs/Amazon_Sales_Dashboard.xlsx`

Visualization output:

`outputs/visualizations/`

The city map in the Excel dashboard is a static image. Run the dashboard sheet script again to refresh it.

### Step 5: Open the Power BI Dashboard

Open the following file using Power BI Desktop:

`powerbi/main_dashboard_amazon1.pbix`

Refresh the data source after updating the cleaned CSV to update the dashboard. Check that the CSV source path is correct on your computer.

## 10. Python Scripts Description

| Script | Description |
|---|---|
| `01_generate_raw_data.py` | Generates the raw synthetic sales dataset. |
| `02_clean_data.py` | Performs data cleaning and transformation. |
| `03_prepare_excel_data.py` | Creates the Excel-ready dataset with helper columns. |
| `04_build_excel.py` | Creates the Excel workbook and summary sheets. |
| `05_dashboard_sheet.py` | Creates the Excel dashboard sheet. |
| `06_visualizations.py` | Generates Matplotlib charts. |

## 11. SQL Analysis

The project includes 12 MySQL queries to analyse sales performance.

The queries cover:

1. Overall sales KPIs.
2. Revenue by category.
3. Revenue by region.
4. Monthly revenue trends.
5. Top 10 products by revenue.
6. Payment-mode distribution.
7. Order-status breakdown.
8. Discount band effectiveness.
9. One-time versus repeat customers.
10. Quarterly revenue.
11. Ratings, return rates, and cancellation rates by category.
12. Top 5 cities by revenue.

### SQL Concepts Used

- SELECT, WHERE, ORDER BY, and DISTINCT.
- Aggregate functions such as SUM, COUNT, and AVG.
- GROUP BY and HAVING.
- CASE WHEN.
- Joins and subqueries, where applicable.
- Date-based analysis.
- Customer and sales performance analysis.

## 12. Power BI DAX Measures

The following measures are used for KPI calculations.

**Total Orders**

```dax
Total Orders =
DISTINCTCOUNT('amazon_sales_clean csv'[Order_ID])
```

**Net Revenue**

```dax
Net Revenue =
SUM('amazon_sales_clean csv'[Net_Revenue])
```

**Average Order Value**

```dax
Average Order Value =
DIVIDE(
    [Net Revenue],
    [Total Orders]
)
```

**Completion Rate**

```dax
Completion Rate =
DIVIDE(
    CALCULATE(
        [Total Orders],
        'amazon_sales_clean csv'[Order_Status] = "Delivered"
    ),
    [Total Orders]
)
```

**Return Rate**

```dax
Return Rate =
DIVIDE(
    CALCULATE(
        [Total Orders],
        'amazon_sales_clean csv'[Order_Status] = "Returned"
    ),
    [Total Orders]
)
```

**Cancellation Rate**

```dax
Cancel Rate =
DIVIDE(
    CALCULATE(
        [Total Orders],
        'amazon_sales_clean csv'[Order_Status] = "Cancelled"
    ),
    [Total Orders]
)
```

**Unique Buyers**

```dax
Unique Buyers =
DISTINCTCOUNT('amazon_sales_clean csv'[Customer_ID])
```

**Average Rating**

```dax
Average Rating =
AVERAGE('amazon_sales_clean csv'[Rating])
```

**Cities Covered**

```dax
Cities Covered =
CALCULATE(
    DISTINCTCOUNT('amazon_sales_clean csv'[City]),
    'amazon_sales_clean csv'[City] <> "Unknown"
)
```

> **Note:** Replace `'amazon_sales_clean csv'` with the exact table name shown in the Power BI Fields pane if your imported table has a different name. Format revenue measures as INR currency and rate measures as percentages.

## 13. Data Quality and Validation

The cleaned dataset is checked for:

- Duplicate order IDs.
- Missing values.
- Invalid dates.
- Non-positive quantities and unit prices.
- Revenue calculation consistency.
- Valid order status values.

These checks help ensure that the cleaned data is suitable for SQL analysis and dashboard reporting.

## 14. Limitations

- The dataset is synthetic and does not represent actual Amazon business performance.
- The project is intended for learning and portfolio demonstration.
- Missing ratings are imputed using the category median, which may influence rating analysis.
- Unknown city and payment information limits some geographic and payment-related analysis.
- The Excel city map is a static image rather than an interactive native Excel map.

## 15. Future Improvements

- Automate data refresh and report generation.
- Connect dashboards directly to an updated database.
- Add customer segmentation and cohort analysis.
- Analyse repeat purchases and customer lifetime value.
- Build forecasting models for revenue and order demand.
- Perform deeper analysis of delivery delays, returns, and cancellations.

## 16. Requirements

The Python dependencies are listed in `requirements.txt`.

```text
pandas
numpy
matplotlib
openpyxl
```

Other required software:

- Python 3
- MySQL Server
- MySQL Workbench
- Microsoft Excel
- Power BI Desktop

## 17. Author

PUNITH REDDY

B.Tech – Computer Science and Engineering(AI&ML)

**Technical Skills:** Python, SQL, MySQL, Excel, Power BI, Data Analysis

LinkedIn:https://www.linkedin.com/in/punithreddy07321/

Email:punithreddygutala@gmail.com

---

*This project was created as a Data Analytics portfolio project to demonstrate practical skills in data cleaning, SQL analysis, Excel reporting, Python visualization, and Power BI dashboard development.*
