/* Fetches the customers who have never placed an order based on ANTI JOIN logic using NOT EXISTS CLAUSE*/

--Code:
SELECT
    customer_id,
    customer_name,
    signup_date
FROM dbo.dim_customer c
WHERE NOT EXISTS (
    SELECT 1
    FROM dbo.fact_orders o
    WHERE c.customer_id = o.customer_id
    and order_status='Completed'
);
