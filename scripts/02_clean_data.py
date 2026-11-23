import os
import pandas as pd
import numpy as np

# -----------------------------------------
# Get project folder automatically
# -----------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_DIR = os.path.join(BASE_DIR, "data")

RAW_PATH = os.path.join(DATA_DIR, "amazon_sales_raw.csv")
CLEAN_PATH = os.path.join(DATA_DIR, "amazon_sales_clean.csv")

print("Reading file from:")
print(RAW_PATH)

# Check if file exists
if not os.path.exists(RAW_PATH):
    raise FileNotFoundError(
        f"\nDataset not found!\n\nExpected location:\n{RAW_PATH}\n\n"
        "Please place amazon_sales_raw.csv inside the data folder."
    )

# Load dataset
df = pd.read_csv(RAW_PATH)

print(f"Raw rows loaded: {len(df)}")

# -----------------------------------------
# Standardize text columns
# -----------------------------------------
for col in ["Category", "Region", "City"]:
    df[col] = (
        df[col]
        .fillna("Unknown")
        .astype(str)
        .str.strip()
        .str.title()
    )

df["Payment_Mode"] = (
    df["Payment_Mode"]
    .fillna("Unknown")
    .astype(str)
    .str.strip()
)

# -----------------------------------------
# Parse mixed date formats (explicit, no guessing)
# Raw file contains 3 formats:
#   YYYY-MM-DD   (e.g. 2024-03-08)
#   DD/MM/YYYY   (e.g. 08/03/2024)
#   MM-DD-YYYY   (e.g. 03-08-2024)
# dayfirst=True guesses wrongly for the first and third formats,
# swapping day and month, so each format is parsed on its own.
# -----------------------------------------
date_text = df["Order_Date"].astype(str).str.strip()

is_iso = date_text.str.match(r"^\d{4}-\d{2}-\d{2}$")
is_slash = date_text.str.contains("/", regex=False)
is_mdy = ~is_iso & ~is_slash

parsed = pd.Series(pd.NaT, index=df.index, dtype="datetime64[ns]")
parsed[is_iso] = pd.to_datetime(date_text[is_iso], format="%Y-%m-%d", errors="coerce")
parsed[is_slash] = pd.to_datetime(date_text[is_slash], format="%d/%m/%Y", errors="coerce")
parsed[is_mdy] = pd.to_datetime(date_text[is_mdy], format="%m-%d-%Y", errors="coerce")
df["Order_Date"] = parsed

print("Invalid dates:", df["Order_Date"].isna().sum())

# -----------------------------------------
# Fill missing values
# -----------------------------------------
df["Discount_%"] = df["Discount_%"].fillna(0)

df["Rating"] = (
    df.groupby("Category")["Rating"]
    .transform(lambda x: x.fillna(x.median()))
)

df["Rating"] = df["Rating"].fillna(df["Rating"].median())

# -----------------------------------------
# Remove duplicate Order IDs
# -----------------------------------------
duplicates = df.duplicated(subset="Order_ID").sum()

df = df.drop_duplicates(subset="Order_ID")

print("Duplicates removed:", duplicates)

# -----------------------------------------
# Remove invalid rows
# -----------------------------------------
df = df[(df["Quantity"] > 0) & (df["Unit_Price"] > 0)]

# Remove invalid dates
df = df.dropna(subset=["Order_Date"])

# -----------------------------------------
# Feature Engineering
# -----------------------------------------
df["Gross_Revenue"] = (
    df["Unit_Price"] * df["Quantity"]
).round(2)

df["Discount_Amount"] = (
    df["Gross_Revenue"] * df["Discount_%"] / 100
).round(2)

df["Net_Revenue"] = (
    df["Gross_Revenue"] - df["Discount_Amount"]
).round(2)

df["Year"] = df["Order_Date"].dt.year
df["Month"] = df["Order_Date"].dt.month
df["Month_Name"] = df["Order_Date"].dt.strftime("%b")
df["Quarter"] = df["Order_Date"].dt.quarter

df["Is_Completed"] = (
    df["Order_Status"] == "Delivered"
)

# -----------------------------------------
# Arrange columns
# -----------------------------------------
df = df[
    [
        "Order_ID",
        "Order_Date",
        "Year",
        "Month",
        "Month_Name",
        "Quarter",
        "Customer_ID",
        "Category",
        "Product_Name",
        "Region",
        "City",
        "Unit_Price",
        "Quantity",
        "Discount_%",
        "Discount_Amount",
        "Gross_Revenue",
        "Net_Revenue",
        "Payment_Mode",
        "Order_Status",
        "Is_Completed",
        "Rating",
    ]
]

df = df.sort_values("Order_Date").reset_index(drop=True)

# -----------------------------------------
# Save cleaned data
# -----------------------------------------
os.makedirs(DATA_DIR, exist_ok=True)

df.to_csv(CLEAN_PATH, index=False)

print("\nCleaning completed successfully!")
print(f"Rows: {len(df)}")
print(f"Columns: {len(df.columns)}")
print(f"Saved to: {CLEAN_PATH}")