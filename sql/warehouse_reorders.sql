SELECT
    Warehouse,
    COUNT(*) AS total_products,
    SUM(Reorder_Required) AS reorder_required,
    SUM(Stockout) AS stockouts
FROM inventory
GROUP BY Warehouse
ORDER BY reorder_required DESC;
