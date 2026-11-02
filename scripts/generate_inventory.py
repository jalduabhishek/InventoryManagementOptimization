
import pandas as pd
import numpy as np
from pathlib import Path

# Create reproducible synthetic inventory data
rng = np.random.default_rng(42)

NUM_PRODUCTS = 1000

categories = [
    "Groceries",
    "Beverages",
    "Dairy",
    "Snacks",
    "Personal Care"
]

warehouses = [
    "Delhi",
    "Mumbai",
    "Bangalore",
    "Hyderabad"
]

data = pd.DataFrame({
    "Product_ID": [
        f"P{i:04d}" for i in range(1, NUM_PRODUCTS + 1)
    ],
    "Category": rng.choice(categories, NUM_PRODUCTS),
    "Warehouse": rng.choice(warehouses, NUM_PRODUCTS),
    "Current_Stock": rng.integers(0, 501, NUM_PRODUCTS),
    "Daily_Demand": rng.integers(5, 51, NUM_PRODUCTS),
    "Supplier_Lead_Time_Days": rng.integers(
        1, 11, NUM_PRODUCTS
    ),
    "Unit_Cost_INR": rng.integers(20, 1001, NUM_PRODUCTS)
})

# Estimated stock coverage
data["Days_of_Stock"] = (
    data["Current_Stock"] / data["Daily_Demand"]
).round(2)

# Basic reorder point using demand during lead time
data["Reorder_Point"] = (
    data["Daily_Demand"]
    * data["Supplier_Lead_Time_Days"]
)

# Identify products needing replenishment
data["Reorder_Required"] = (
    data["Current_Stock"] <= data["Reorder_Point"]
)

# Identify products already out of stock
data["Stockout"] = data["Current_Stock"] == 0

# Inventory value
data["Inventory_Value_INR"] = (
    data["Current_Stock"] * data["Unit_Cost_INR"]
)

# Save dataset
project_root = Path(__file__).resolve().parent.parent
output_dir = project_root / "data"
output_dir.mkdir(exist_ok=True)

output_file = output_dir / "inventory_data.csv"
data.to_csv(output_file, index=False)

print("Inventory dataset generated successfully!")
print("Total Products:", len(data))
print("Products Requiring Reorder:",
      data["Reorder_Required"].sum())
print("Stockout Products:", data["Stockout"].sum())
print("Total Inventory Value (INR):",
      data["Inventory_Value_INR"].sum())
print("Saved to:", output_file)
