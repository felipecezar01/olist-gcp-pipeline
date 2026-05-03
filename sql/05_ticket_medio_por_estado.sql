-- Ticket médio e volume de pedidos por estado
SELECT
  c.customer_state AS estado,
  COUNT(*) AS total_pedidos,
  ROUND(AVG(p.payment_value), 2) AS ticket_medio
FROM `olist-pipeline-495119.olist_ecommerce.orders` o
JOIN `olist-pipeline-495119.olist_ecommerce.customers` c
  ON o.customer_id = c.customer_id
JOIN `olist-pipeline-495119.olist_ecommerce.order_payments` p
  ON o.order_id = p.order_id
GROUP BY estado
ORDER BY total_pedidos DESC
LIMIT 10