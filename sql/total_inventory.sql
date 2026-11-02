SELECT
    COUNT(*) AS total_products,
    SUM(Inventory_Value_INR) AS total_inventory_value,
    ROUND(AVG(Days_of_Stock), 2) AS avg_days_of_stock
FROM inventory;
