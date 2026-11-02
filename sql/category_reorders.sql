SELECT
    Category,
    COUNT(*) AS total_products,
    SUM(Reorder_Required) AS reorder_required
FROM inventory
GROUP BY Category
ORDER BY reorder_required DESC;
