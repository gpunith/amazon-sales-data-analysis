"""
Generate a synthetic, realistic-looking raw Amazon sales dataset (10,000+ rows).
Intentionally includes messiness (duplicates, missing values, inconsistent casing,
mixed date formats) so the cleaning step has real work to do.
"""

import os
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# Set random seed
np.random.seed(42)

# Number of records
N = 10500

# Categories and Products
categories = {
    "Electronics": [
        "Wireless Earbuds", "Bluetooth Speaker", "Smartphone Case",
        "Power Bank", "USB-C Cable", "Smartwatch",
        "Laptop Stand", "Webcam"
    ],
    "Home & Kitchen": [
        "Air Fryer", "Non-stick Pan Set", "Electric Kettle",
        "Blender", "Vacuum Cleaner", "Storage Containers",
        "LED Desk Lamp"
    ],
    "Fashion": [
        "Men's T-Shirt", "Women's Kurti", "Running Shoes",
        "Leather Wallet", "Denim Jacket",
        "Sunglasses", "Backpack"
    ],
    "Beauty & Personal Care": [
        "Face Wash", "Hair Dryer", "Trimmer",
        "Moisturizer", "Perfume", "Sunscreen"
    ],
    "Books": [
        "Fiction Novel", "Self-Help Book",
        "Cookbook", "Children's Storybook"
    ],
    "Sports & Fitness": [
        "Yoga Mat", "Dumbbell Set",
        "Resistance Bands", "Cycling Helmet",
        "Fitness Tracker"
    ],
    "Toys & Games": [
        "Building Blocks", "Remote Control Car",
        "Board Game", "Puzzle Set"
    ],
    "Grocery": [
        "Organic Almonds", "Green Tea",
        "Protein Powder", "Cooking Oil 1L"
    ]
}

regions = ["North", "South", "East", "West", "Central"]

cities_by_region = {
    "North": ["Delhi", "Chandigarh", "Lucknow"],
    "South": ["Bengaluru", "Chennai", "Hyderabad"],
    "East": ["Kolkata", "Patna", "Bhubaneswar"],
    "West": ["Mumbai", "Pune", "Ahmedabad"],
    "Central": ["Bhopal", "Nagpur", "Raipur"]
}

payment_modes = [
    "Credit Card",
    "Debit Card",
    "UPI",
    "Net Banking",
    "Cash on Delivery",
    "Amazon Pay"
]

order_status_pool = [
    "Delivered",
    "Delivered",
    "Delivered",
    "Delivered",
    "Cancelled",
    "Returned",
    "Pending"
]

start_date = datetime(2023, 1, 1)
end_date = datetime(2024, 12, 31)
date_range_days = (end_date - start_date).days

base_prices = {
    "Electronics": (500, 4500),
    "Home & Kitchen": (400, 6000),
    "Fashion": (250, 3000),
    "Beauty & Personal Care": (150, 1800),
    "Books": (150, 900),
    "Sports & Fitness": (300, 4000),
    "Toys & Games": (200, 2500),
    "Grocery": (100, 1200),
}

rows = []

for i in range(N):

    category = np.random.choice(
        list(categories.keys()),
        p=[0.22, 0.15, 0.18, 0.12, 0.08, 0.10, 0.08, 0.07]
    )

    product = np.random.choice(categories[category])

    region = np.random.choice(regions)
    city = np.random.choice(cities_by_region[region])

    lo, hi = base_prices[category]
    unit_price = round(np.random.uniform(lo, hi), 2)

    quantity = int(
        np.random.choice(
            [1, 1, 1, 2, 2, 3, 4, 5],
            p=[0.35, 0.20, 0.10, 0.15, 0.08, 0.06, 0.04, 0.02]
        )
    )

    discount = np.random.choice(
        [0, 5, 10, 15, 20, 25, 30],
        p=[0.25, 0.15, 0.20, 0.15, 0.12, 0.08, 0.05]
    )

    order_date = start_date + timedelta(
        days=int(np.random.uniform(0, date_range_days))
    )

    rating = np.random.choice(
        [1, 2, 3, 4, 5, np.nan],
        p=[0.03, 0.05, 0.12, 0.35, 0.40, 0.05]
    )

    status = np.random.choice(order_status_pool)

    # Random casing
    category_display = (
        category if np.random.rand() > 0.15 else category.upper()
    )

    region_display = (
        region if np.random.rand() > 0.10 else region.lower()
    )

    # Mixed date formats
    r = np.random.rand()

    if r < 0.70:
        date_string = order_date.strftime("%Y-%m-%d")
    elif r < 0.90:
        date_string = order_date.strftime("%d/%m/%Y")
    else:
        date_string = order_date.strftime("%m-%d-%Y")

    rows.append({
        "Order_ID": f"AMZ{100000+i}",
        "Order_Date": date_string,
        "Customer_ID": f"CUST{np.random.randint(1000,4000)}",
        "Category": category_display,
        "Product_Name": product,
        "Region": region_display,
        "City": city,
        "Unit_Price": unit_price,
        "Quantity": quantity,
        "Discount_%": discount,
        "Payment_Mode": np.random.choice(payment_modes),
        "Order_Status": status,
        "Rating": rating
    })

# Create DataFrame
df = pd.DataFrame(rows)

# Introduce missing values
for col in ["Rating", "City", "Payment_Mode", "Discount_%"]:
    mask = np.random.rand(len(df)) < 0.03
    df.loc[mask, col] = np.nan

# Add duplicate rows
duplicates = df.sample(250, random_state=1)
df = pd.concat([df, duplicates], ignore_index=True)

# Introduce data entry errors
error_idx = df.sample(15, random_state=2).index

df.loc[error_idx[:8], "Quantity"] = -1
df.loc[error_idx[8:], "Unit_Price"] = 0

# Shuffle dataset
df = df.sample(frac=1, random_state=3).reset_index(drop=True)

# Create data folder
os.makedirs("data", exist_ok=True)

# Save CSV
output_path = "data/amazon_sales_raw.csv"
df.to_csv(output_path, index=False)

print(f"Dataset generated successfully!")
print(f"Rows: {len(df)}")
print(f"Saved to: {output_path}")
print(df.head())