import os
import pandas as pd

# =====================================================
# Project Paths
# =====================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_DIR = os.path.join(BASE_DIR, "data")

CLEAN_PATH = os.path.join(DATA_DIR, "amazon_sales_clean.csv")
EXCEL_DATA_PATH = os.path.join(DATA_DIR, "amazon_sales_for_excel.csv")

print("Reading:", CLEAN_PATH)

# =====================================================
# Check if file exists
# =====================================================
if not os.path.exists(CLEAN_PATH):
    raise FileNotFoundError(
        f"Clean dataset not found!\nExpected:\n{CLEAN_PATH}"
    )

# =====================================================
# Load Clean Data
# =====================================================
df = pd.read_csv(CLEAN_PATH, parse_dates=["Order_Date"])

print(f"Rows Loaded : {len(df)}")

# =====================================================
# Customer Order Count
# =====================================================
df["Customer_Order_Count"] = (
    df.groupby("Customer_ID")["Order_ID"]
      .transform("count")
)

# =====================================================
# Customer Type
# =====================================================
df["Customer_Type"] = df["Customer_Order_Count"].apply(
    lambda x: "One-time" if x == 1 else "Repeat"
)

# =====================================================
# Discount Band
# =====================================================
def discount_band(discount):

    if discount == 0:
        return "0% (No Discount)"

    elif discount <= 10:
        return "1-10%"

    elif discount <= 20:
        return "11-20%"

    else:
        return "21%+"

df["Discount_Band"] = df["Discount_%"].apply(discount_band)

# =====================================================
# Save File
# =====================================================
df.to_csv(EXCEL_DATA_PATH, index=False)

print("\n===================================")
print("Excel Dataset Created Successfully")
print("===================================")
print(f"Rows : {len(df)}")
print(f"Columns : {len(df.columns)}")
print(f"Saved To : {EXCEL_DATA_PATH}")