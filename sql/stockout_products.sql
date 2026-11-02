SELECT
    Product_ID,
    Warehouse,
    Category,
    Daily_Demand,
    Supplier_Lead_Time_Days
FROM inventory
WHERE Stockout = 1
ORDER BY Daily_Demand DESC;
