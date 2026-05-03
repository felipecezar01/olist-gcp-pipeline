-- Tempo médio de entrega por estado
SELECT
  c.customer_state AS estado,
  COUNT(*) AS total_pedidos,
  ROUND(AVG(
    DATE_DIFF(DATE(o.order_delivered_customer_date),
    DATE(o.order_purchase_timestamp), DAY)
  ), 1) AS prazo_medio_dias
FROM `olist-pipeline-495119.olist_ecommerce.orders` o
JOIN `olist-pipeline-495119.olist_ecommerce.customers` c
  ON o.customer_id = c.customer_id
WHERE o.order_status = 'delivered'
  AND o.order_delivered_customer_date IS NOT NULL
GROUP BY estado
ORDER BY prazo_medio_dias DESC