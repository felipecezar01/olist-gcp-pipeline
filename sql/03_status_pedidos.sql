-- Distribuição de status dos pedidos
SELECT
  order_status,
  COUNT(*) AS total,
  ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) AS percentual
FROM `olist-pipeline-495119.olist_ecommerce.orders`
GROUP BY order_status
ORDER BY total DESC