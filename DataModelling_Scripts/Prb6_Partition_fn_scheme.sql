--Step 1 -> Creating a Partition function for factsales table
CREATE PARTITION FUNCTION pf_FactTicketSales (INT)
AS RANGE RIGHT FOR VALUES
(
    20240101,
    20250101,
    20260101,
    20270101
);
GO

--Step 2 -> Creating a Partition scheme
CREATE PARTITION SCHEME ps_FactTicketSales
AS PARTITION pf_FactTicketSales
ALL TO ([PRIMARY]);
GO

--Step 3 -> Since table already exists creating a index into the partition scheme
--Step 3.1 -> Dropping the existing clustered index
ALTER TABLE dw.FactTicketSales
DROP CONSTRAINT PK__FactTick__5DE3A5B157B0B376;
GO

--Step 3.2 -> Creating a new clustered index based on the new partition scheme
CREATE CLUSTERED INDEX CIX_FactTicketSales
ON dw.FactTicketSales(travel_date_key, booking_id)
ON ps_FactTicketSales(travel_date_key);
GO


-- Step 4 -> recreating the primary key on the partition scheme
ALTER TABLE dw.FactTicketSales
ADD CONSTRAINT PK_FactTicketSales
PRIMARY KEY CLUSTERED
(
    travel_date_key,
    booking_id
)
ON ps_FactTicketSales(travel_date_key);
GO

-- Step 5 : Running the query based on Partition column and capturing Execution Plan
SELECT *
FROM dw.FactTicketSales
WHERE travel_date_key BETWEEN 20250101 AND 20250131;
--Actual Partition count - 1
--Actual Partition accessed - 3

--Step 6 : Running the query without Partition column and capturing Execution Plan
SELECT *
FROM dw.FactTicketSales
WHERE passenger_key = 1050;
--Actual Partition count - 5
--Actual Partition accessed - 1 .. 5




