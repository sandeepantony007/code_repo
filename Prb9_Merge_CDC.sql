use Voltkart

/*MERGE _ CDC Implemenation */

/*----------------------------------------------------
1. Enable CDC at Database Level
----------------------------------------------------*/
IF NOT EXISTS (
    SELECT 1
    FROM sys.databases
    WHERE name = DB_NAME()
      AND is_cdc_enabled = 1
)
BEGIN
    EXEC sys.sp_cdc_enable_db;
END
GO

/*----------------------------------------------------
2. Enable CDC for dim_product Table
----------------------------------------------------*/
IF NOT EXISTS (
    SELECT 1
    FROM cdc.change_tables
    WHERE source_object_id = OBJECT_ID('dbo.dim_product')
)
BEGIN
    EXEC sys.sp_cdc_enable_table
        @source_schema = 'dbo',
        @source_name = 'dim_product',
        @role_name = NULL,
        @supports_net_changes = 0;
END
GO


/*----------------------------------------------------
3. MERGE Stattement with CDC
----------------------------------------------------*/
MERGE dbo.dim_product AS T
USING dbo.cdc_product_changes AS S
ON T.product_id = S.product_id

WHEN MATCHED
    AND S.operation = 'U'
THEN
    UPDATE SET
        T.product_name = S.product_name,
        T.category_id  = S.category_id,
        T.unit_price   = S.unit_price,
        T.unit_cost    = S.unit_cost,
        T.launch_date  = S.launch_date

WHEN MATCHED
    AND S.operation = 'D'
THEN
    DELETE

WHEN NOT MATCHED BY TARGET
    AND S.operation = 'I'
THEN
    INSERT
    (
        product_id,product_name,category_id,unit_price,unit_cost,launch_date)
    VALUES
    (
        S.product_id,S.product_name,S.category_id,S.unit_price,S.unit_cost,S.launch_date);


/*----------------------------------------------------
4. View CDC Changes
----------------------------------------------------*/
SELECT
    S.operation AS CDC_Action,
    S.product_id,
    S.product_name AS CDC_Product_Name,
    T.product_name AS Current_Product_Name,
    CASE
        WHEN S.operation = 'I' AND T.product_id IS NOT NULL THEN 'Inserted'
        WHEN S.operation = 'U' AND T.product_id IS NOT NULL THEN 'Updated'
        WHEN S.operation = 'D' AND T.product_id IS NULL THEN 'Deleted'
        ELSE 'Check'
    END AS Merge_Result
FROM dbo.cdc_product_changes S
LEFT JOIN dbo.dim_product T
    ON S.product_id = T.product_id
ORDER BY S.operation, S.product_id;




/*----------------------------------------------------
4. View CDC Changes - Internal CDC table
----------------------------------------------------*/
SELECT
    CASE __$operation
        WHEN 1 THEN 'DELETE'
        WHEN 2 THEN 'INSERT'
        WHEN 3 THEN 'UPDATE_BEFORE'
        WHEN 4 THEN 'UPDATE_AFTER'
    END AS OperationType,
    product_id,
    product_name,
    category_id,
    unit_price,
    unit_cost,
    __$start_lsn
FROM cdc.dbo_dim_product_CT
WHERE product_id in (900033,950001,900031)
ORDER BY __$start_lsn;
GO