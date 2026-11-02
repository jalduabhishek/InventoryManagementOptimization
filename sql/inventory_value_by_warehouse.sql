SELECT
    Warehouse,
    SUM(Inventory_Value_INR) AS inventory_value
FROM inventory
GROUP BY Warehouse
ORDER BY inventory_value DESC;
