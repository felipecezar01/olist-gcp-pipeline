-- Top 10 categorias por receita e volume
SELECT
  t.string_field_1 AS categoria,
  COUNT(DISTINCT oi.order_id) AS total_pedidos,
  ROUND(SUM(oi.price), 2) AS receita_total,
  ROUND(AVG(r.review_score), 2) AS nota_media
FROM `olist-pipeline-495119.olist_ecommerce.order_items` oi
JOIN `olist-pipeline-495119.olist_ecommerce.products` p
  ON oi.product_id = p.product_id
JOIN `olist-pipeline-495119.olist_ecommerce.product_category_translation` t
  ON p.product_category_name = t.string_field_0
JOIN `olist-pipeline-495119.olist_ecommerce.order_reviews` r
  ON oi.order_id = r.order_id
GROUP BY categoria
ORDER BY receita_total DESC
LIMIT 10