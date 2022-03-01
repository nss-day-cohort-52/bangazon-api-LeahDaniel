SELECT o.id,
    u.first_name || " " || u.last_name customer_name,
    SUM(p.price) total_cost,
    pt.merchant_name
FROM bangazon_api_order o 
JOIN auth_user u ON o.user_id = u.id
JOIN bangazon_api_orderproduct op ON op.order_id = o.id
JOIN bangazon_api_product p ON p.id = op.product_id
JOIN bangazon_api_paymenttype pt ON o.payment_type_id = pt.id
WHERE o.completed_on NOTNULL
GROUP BY o.id
ORDER BY o.created_on