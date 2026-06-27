WITH orders AS (
    SELECT
        order_id,
        order_date,
        order_total,
        customer_id,
        sales_rep_id,
        RANK() OVER (ORDER BY order_total DESC) AS rnk
    FROM dbo.fact_orders
    where order_status='Completed'
)
SELECT
    o.order_id,
    o.order_date,
    c.customer_name,
    e.employee_name AS sales_rep_name,
    o.order_total
FROM orders o
LEFT JOIN dbo.dim_employee e
    ON o.sales_rep_id = e.employee_id
   AND e.role = 'Sales Rep'
LEFT JOIN dbo.dim_customer c
    ON o.customer_id=c.customer_id
WHERE o.rnk <= 20;