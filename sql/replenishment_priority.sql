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
