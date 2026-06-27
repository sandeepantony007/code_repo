/*This query fetches month over month revenue trend and the cumulating running total as of the reporting month.

Uses CTE to find the monthly revenue and windows frame to sum current and previous value to get the running total.
Uses LAG function to derive the month over month revenue trend

*/

WITH monthly_revenue AS (
    SELECT
        DATEFROMPARTS(YEAR(order_date), MONTH(order_date), 1) AS month_start,
        ROUND(SUM(order_total),2) AS monthly_revenue
    FROM fact_orders
    WHERE order_status = 'Completed'
    GROUP BY DATEFROMPARTS(YEAR(order_date), MONTH(order_date), 1)
)
SELECT
    CONVERT(char(7), month_start, 120) AS order_month,
    monthly_revenue,  
    SUM(monthly_revenue) OVER (
        ORDER BY month_start
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_total,   
    ROUND(
        ( 
            (monthly_revenue -
                LAG(monthly_revenue) OVER (ORDER BY month_start)
            ) * 100.0
        ) /
        NULLIF(
            LAG(monthly_revenue) OVER (ORDER BY month_start), 0  
			),
        2
    ) AS mom_pct_change
FROM monthly_revenue
ORDER BY month_start;