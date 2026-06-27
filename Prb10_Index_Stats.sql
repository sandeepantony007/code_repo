--existing query
SELECT o.customer_id, COUNT(*) AS orders_2024, 
	(SELECT SUM(oi.line_amount) FROM fact_order_items oi JOIN fact_orders o2 ON o2.order_id = oi.order_id 
	WHERE o2.customer_id = o.customer_id) AS lifetime_value 
FROM fact_orders 
o WHERE YEAR(o.order_date) = 2024 
GROUP BY o.customer_id
order by o.customer_id;

/* Execution Plan before Optimization
Performs full table scan due to Year extract filter
Performs table scans multiple times due to correlated subquery for each record
performs aggregation multiple times
Due to YEAR extraction logic not able to use Index on the date column
Cost of execution is more due to repeated aggreation and joins
*/

--Index Creation
CREATE INDEX IX_fact_orders_order_date
    ON dbo.fact_orders(order_date, customer_id);

/* -- New Optimized Query Execution
Optimized query by aggregating and joining Once
changing the YEAR value to date so Index can be used
Index created for Faster Processing
*/

WITH orders_2024 AS
(
    SELECT
        customer_id,
        COUNT(*) AS orders_2024
    FROM dbo.fact_orders
    WHERE order_date >= '2024-01-01'
      AND order_date < '2025-01-01'
    GROUP BY customer_id
),
lifetime_value AS
(
    SELECT
        o.customer_id,
        SUM(oi.line_amount) AS lifetime_value
    FROM dbo.fact_orders o
    INNER JOIN dbo.fact_order_items oi
        ON o.order_id = oi.order_id
    GROUP BY o.customer_id
)
SELECT
    o.customer_id,
    o.orders_2024,
    COALESCE(l.lifetime_value, 0) AS lifetime_value
FROM orders_2024 o
LEFT JOIN lifetime_value l
    ON o.customer_id = l.customer_id
ORDER BY o.customer_id;


/* Execution Plan after Optimization
Performs full table scan only once (scans fact_orders) and data sorted earlier
Lifetime value calculated once using aggregation
Uses a date range intead of YEAR along, allowing an index seek

*/