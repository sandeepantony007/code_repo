/*
This query used to traverse and list all the categories under the sub category -> Computers

User recursive CTE process to have Anchor as "Computers" subcategory and traverse all its sub category using recursive CTE
Finally have a termination join condition to get the full list
*/

WITH category_tree AS (
    -- Anchor
    SELECT
        category_id,
        parent_category_id,
        category_name,
        1 AS depth,
        CAST(category_name AS NVARCHAR(MAX)) AS category_path
    FROM dim_category
    WHERE category_name = 'Computers'

    UNION ALL

    -- Recursive
    SELECT
        dc.category_id,
        dc.parent_category_id,
        dc.category_name,
        ct.depth + 1,
        CAST(ct.category_path + ' -> ' + dc.category_name AS NVARCHAR(MAX))
    FROM dim_category dc
    INNER JOIN category_tree ct
        ON dc.parent_category_id = ct.category_id --Termination condition
)
SELECT *
FROM category_tree
ORDER BY depth;