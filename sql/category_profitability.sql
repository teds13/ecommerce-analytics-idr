SELECT
  Category,
  Total_SKU,
  Total_Units_Sold,
  Total_Revenue_IDR,
  Total_Profit_IDR,
  ROUND(Avg_Rating, 2) AS Avg_Rating
FROM `ecommerce-analytics-id.ecommerce_idr.category_summary`
ORDER BY Total_Profit_IDR DESC;