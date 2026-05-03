-- Receita mensal ao longo do tempo
SELECT
  FORMAT_DATE('%Y-%m', DATE(o.order_purchase_timestamp)) AS mes,
  COUNT(DISTINCT o.order_id) AS total_pedidos,
  ROUND(SUM(p.payment_value), 2) AS receita_total
FROM `olist-pipeline-495119.olist_ecommerce.orders` o
JOIN `olist-pipeline-495119.olist_ecommerce.order_payments` p
  ON o.order_id = p.order_id
WHERE o.order_status = 'delivered'
GROUP BY mes
ORDER BY mes