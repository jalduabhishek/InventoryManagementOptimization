
import pandas as pd
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent

df = pd.read_csv(
    project_root / "data" / "inventory_data.csv"
)

print("\n===== INVENTORY PERFORMANCE =====")

print("Total Products:", len(df))

print(
    "Products Requiring Reorder:",
    df["Reorder_Required"].sum()
)

print(
    "Reorder Rate:",
    round(df["Reorder_Required"].mean() * 100, 2),
    "%"
)

print(
    "Out-of-Stock Products:",
    df["Stockout"].sum()
)

print(
    "Total Inventory Value (INR):",
    df["Inventory_Value_INR"].sum()
)

print(
    "Average Days of Stock:",
    round(df["Days_of_Stock"].mean(), 2)
)

print("\n===== WAREHOUSE PERFORMANCE =====")

warehouse = df.groupby("Warehouse").agg(
    Total_Products=("Product_ID", "count"),
    Reorder_Required=("Reorder_Required", "sum"),
    Stockouts=("Stockout", "sum"),
    Inventory_Value_INR=("Inventory_Value_INR", "sum")
)

print(warehouse.to_string())

print("\n===== CATEGORY PERFORMANCE =====")

category = df.groupby("Category").agg(
    Total_Products=("Product_ID", "count"),
    Reorder_Required=("Reorder_Required", "sum"),
    Inventory_Value_INR=("Inventory_Value_INR", "sum")
)

print(category.to_string())

print("\n===== TOP 10 REPLENISHMENT PRIORITIES =====")

priority = df[df["Reorder_Required"]].copy()

priority = priority.sort_values(
    ["Days_of_Stock", "Supplier_Lead_Time_Days"],
    ascending=[True, False]
)

print(
    priority[
        [
            "Product_ID",
            "Warehouse",
            "Current_Stock",
            "Daily_Demand",
            "Days_of_Stock",
            "Supplier_Lead_Time_Days"
        ]
    ].head(10).to_string(index=False)
)
