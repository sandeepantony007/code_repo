/*This query fetches the top 3 highest revenue-generating products within each product category based on completed orders.

Joins fact_order_items, fact_orders, dim_product, and dim_category to combine order, product, and category details
uses sum to find the total revenue and row_number function to fetch the top 3 products with highest revenue.
*/

--Code:
Select * from ( 
        SELECT
            c.category_name,
            p.product_name,
            SUM(ot.line_amount) AS total_Revenue,
            row_number() OVER (partition by c.category_name
                ORDER BY SUM(ot.line_amount) DESC
            ) AS revenue_rank
        FROM dbo.fact_order_items ot
        INNER JOIN dbo.fact_orders o
            ON ot.order_id = o.order_id
        INNER JOIN dbo.dim_product p
            ON p.product_id=ot.product_id
        INNER JOIN dbo.dim_category c
            ON c.category_id=p.category_id
        WHERE o.order_status = 'Completed'
        GROUP BY
            c.category_name,
            p.product_name ) top_prod
   where top_prod.revenue_rank<=3
