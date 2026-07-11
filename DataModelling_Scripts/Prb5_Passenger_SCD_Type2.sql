/* Rebuilding Passenger dimension table with scd type 2 columns(effective from and to dates and active status column)*/

--Step 1 : Modify the tables to have effective dates and active status column
ALTER TABLE dw.DimPassenger
ADD
    effective_from DATE NULL,
    effective_to DATE NULL,
    is_current BIT NULL;
GO

-- Step 2 : Updated the effective dates and current status as active for the already loaded records
UPDATE dw.DimPassenger
SET
    effective_from = GETDATE(),
    effective_to = NULL,
    is_current = 1;
GO

--Step 3 : Checking the rebuilt Passenger Dimension tables with SCD Type 2 columns
Select * from dw.DimPassenger;


--Step 4 : Update effective date and active status column to expire records where updated values present in stage table
UPDATE dp
SET
    dp.effective_to = CAST(GETDATE() AS DATE),
    dp.is_current = 0
FROM dw.DimPassenger dp
INNER JOIN stg_passenger_updates s
    ON dp.passenger_id = s.passenger_id
WHERE dp.is_current = 1
AND (
       ISNULL(dp.frequent_flyer_tier,'') <> ISNULL(s.frequent_flyer_tier,'')
    OR ISNULL(dp.home_airport_code,'') <> ISNULL(s.home_airport_code,'')
);
GO


--Step 5  : Insert new and updated records with active status and 1
INSERT INTO dw.DimPassenger
(
    passenger_id,
    passenger_name,
    home_airport_code,
    frequent_flyer_tier,
    signup_date,
    effective_from,
    effective_to,
    is_current
)
SELECT
    s.passenger_id,
    s.passenger_name,
    s.home_airport_code,
    s.frequent_flyer_tier,
    bp.signup_date,
    CAST(GETDATE() AS DATE),
    NULL,
    1
FROM stg_passenger_updates s
LEFT JOIN bronze_passengers bp
       ON s.passenger_id = bp.passenger_id
LEFT JOIN dw.DimPassenger dp
       ON dp.passenger_id = s.passenger_id
      AND dp.is_current = 1
WHERE dp.passenger_id IS NULL
   OR (
          ISNULL(dp.frequent_flyer_tier,'') <> ISNULL(s.frequent_flyer_tier,'')
       OR ISNULL(dp.home_airport_code,'') <> ISNULL(s.home_airport_code,'')
      );
GO



--Step 6 : Validate the Passenger Dimension table post updates
SELECT
*
FROM dw.DimPassenger
ORDER BY passenger_id, effective_from;