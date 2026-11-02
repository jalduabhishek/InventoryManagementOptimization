
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent

df = pd.read_csv(
    project_root / "data" / "inventory_data.csv"
)

reports = project_root / "reports"
reports.mkdir(exist_ok=True)

# Chart 1: Reorder requirements by warehouse
warehouse_reorders = (
    df.groupby("Warehouse")["Reorder_Required"]
    .sum()
    .sort_values(ascending=False)
)

plt.figure(figsize=(9, 5))
warehouse_reorders.plot(kind="bar", color="steelblue")
plt.title("Products Requiring Reorder by Warehouse")
plt.xlabel("Warehouse")
plt.ylabel("Number of Products")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(reports / "warehouse_reorders.png")
plt.close()

# Chart 2: Reorder requirements by category
category_reorders = (
    df.groupby("Category")["Reorder_Required"]
    .sum()
    .sort_values(ascending=False)
)

plt.figure(figsize=(9, 5))
category_reorders.plot(kind="bar", color="darkorange")
plt.title("Reorder Requirements by Product Category")
plt.xlabel("Category")
plt.ylabel("Number of Products")
plt.xticks(rotation=25)
plt.tight_layout()
plt.savefig(reports / "category_reorders.png")
plt.close()

# Chart 3: Inventory value by warehouse
warehouse_value = (
    df.groupby("Warehouse")["Inventory_Value_INR"]
    .sum()
    .sort_values(ascending=False)
)

plt.figure(figsize=(9, 5))
warehouse_value.plot(kind="bar", color="seagreen")
plt.title("Inventory Value by Warehouse")
plt.xlabel("Warehouse")
plt.ylabel("Inventory Value (INR)")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(reports / "warehouse_inventory_value.png")
plt.close()

# Chart 4: Stockout distribution
stockout_counts = df["Stockout"].value_counts()

plt.figure(figsize=(7, 5))
plt.pie(
    stockout_counts.values,
    labels=[
        "Out of Stock" if value else "In Stock"
        for value in stockout_counts.index
    ],
    autopct="%1.1f%%",
    startangle=90
)
plt.title("Stockout Distribution")
plt.tight_layout()
plt.savefig(reports / "stockout_distribution.png")
plt.close()

print("All inventory charts generated successfully!")
print("Charts saved in:", reports)
