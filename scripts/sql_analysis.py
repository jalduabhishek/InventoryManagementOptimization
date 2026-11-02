
import pandas as pd
import sqlite3
from pathlib import Path

# Project paths
project_root = Path(__file__).resolve().parent.parent
data_dir = project_root / "data"
sql_dir = project_root / "sql"

sql_dir.mkdir(exist_ok=True)

# Load synthetic inventory dataset
df = pd.read_csv(data_dir / "inventory_data.csv")

# Create SQLite database
db_path = data_dir / "inventory.db"

with sqlite3.connect(db_path) as conn:

    df.to_sql(
        "inventory",
        conn,
        if_exists="replace",
        index=False
    )

    queries = {
        "total_inventory.sql": """
SELECT
    COUNT(*) AS total_products,
    SUM(Inventory_Value_INR) AS total_inventory_value,
    ROUND(AVG(Days_of_Stock), 2) AS avg_days_of_stock
FROM inventory;
""",

        "warehouse_reorders.sql": """
SELECT
    Warehouse,
    COUNT(*) AS total_products,
    SUM(Reorder_Required) AS reorder_required,
    SUM(Stockout) AS stockouts
FROM inventory
GROUP BY Warehouse
ORDER BY reorder_required DESC;
""",

        "category_reorders.sql": """
SELECT
    Category,
    COUNT(*) AS total_products,
    SUM(Reorder_Required) AS reorder_required
FROM inventory
GROUP BY Category
ORDER BY reorder_required DESC;
""",

        "stockout_products.sql": """
SELECT
    Product_ID,
    Warehouse,
    Category,
    Daily_Demand,
    Supplier_Lead_Time_Days
FROM inventory
WHERE Stockout = 1
ORDER BY Daily_Demand DESC;
""",

        "replenishment_priority.sql": """
SELECT
    Product_ID,
    Warehouse,
    Current_Stock,
    Daily_Demand,
    Days_of_Stock,
    Supplier_Lead_Time_Days,
    Reorder_Point
FROM inventory
WHERE Reorder_Required = 1
ORDER BY
    Days_of_Stock ASC,
    Supplier_Lead_Time_Days DESC
LIMIT 10;
""",

        "inventory_value_by_warehouse.sql": """
SELECT
    Warehouse,
    SUM(Inventory_Value_INR) AS inventory_value
FROM inventory
GROUP BY Warehouse
ORDER BY inventory_value DESC;
"""
    }

    # Save and execute each SQL query
    for filename, query in queries.items():

        (sql_dir / filename).write_text(
            query.strip() + "\n",
            encoding="utf-8"
        )

        result = pd.read_sql_query(query, conn)

        print(f"\n===== {filename} =====")
        print(result.to_string(index=False))

print("\nSQL inventory analysis completed successfully!")
print("Database saved to:", db_path)
print("SQL queries saved to:", sql_dir)
