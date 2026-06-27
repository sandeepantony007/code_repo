/*This query fetches the lifetime completed spend with segregation of four quartiles.

For each customer identified the lifetime_spend of completed orders using CTE and sum function from fact_orders table 
Used NTILE function to split into 4 quartiles based on lifetime_spend
Then derived the count and average based on the above split.

*/

WITH customer_spend AS (
    SELECT
        customer_id,
        SUM(order_total) AS lifetime_spend
    FROM dbo.fact_orders
    WHERE order_status = 'Completed'
    GROUP BY customer_id
),
customer_quartiles AS (
    SELECT
        customer_id,
        lifetime_spend,
        NTILE(4) OVER (ORDER BY lifetime_spend) AS spend_quartile
    FROM customer_spend
)
SELECT
    spend_quartile,
    COUNT(*) AS customer_count,
    ROUND(AVG(lifetime_spend), 2) AS avg_lifetime_spend
FROM customer_quartiles
GROUP BY spend_quartile
ORDER BY spend_quartile;