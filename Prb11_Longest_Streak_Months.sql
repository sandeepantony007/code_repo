/*This query finds the longest streak of consecutive calendar months in which each customer placed at least one completed order, it uses Common Table Expressions (CTEs) and window functions to find,

Unique months in which each customer placed a completed order
Creates a grouping key that identifies consecutive months.
Joins all customers with their streaks and returns the maximum streak length for each customer.*/

WITH customer_months AS
(
    -- One row per customer per completed-order month
    SELECT DISTINCT
        o.customer_id,
        DATEFROMPARTS(YEAR(o.order_date), MONTH(o.order_date), 1) AS order_month
    FROM dbo.fact_orders o
    WHERE o.order_status = 'Completed'
),

numbered_months AS
(
    SELECT
        customer_id,
        order_month,
        ROW_NUMBER() OVER
        (
            PARTITION BY customer_id
            ORDER BY order_month
        ) AS rn
    FROM customer_months
),

month_groups AS
(
    SELECT
        customer_id,
        order_month,
        DATEADD
        (
            MONTH,
            -rn,
            order_month
        ) AS grp
    FROM numbered_months
),

streaks AS
(
    SELECT
        customer_id,
        grp,
        COUNT(*) AS streak_months
    FROM month_groups
    GROUP BY
        customer_id,
        grp
)

SELECT
    c.customer_id,
    c.customer_name,
    MAX(s.streak_months) AS longest_streak_months
FROM dbo.dim_customer c
LEFT JOIN streaks s
    ON c.customer_id = s.customer_id
GROUP BY
    c.customer_id,
    c.customer_name
ORDER BY
    c.customer_id;
