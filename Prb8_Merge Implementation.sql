/*
This query is used to perform Incremental load update and inserts using Merge statement

*--- Before Merge Implementation - Count check and samples
Select count(*) from dbo.fact_orders; Record  Count -> 30000

Select fo.* from dbo.fact_orders fo
where fo.order_id in (6000076, 6000099, 6000166) 
6000076	2023-03-20	500023	23	Completed	23183.25
6000099	2023-12-29	500105	37	Completed	26749.580078125
6000166	2024-01-24	500063	29	Returned	102821.0078125
*/

--Implementation
MERGE INTO dbo.fact_orders AS tgt
USING dbo.stg_orders_incr AS src
ON tgt.order_id = src.order_id

WHEN MATCHED AND (
		ISNULL(tgt.order_status,'') <> ISNULL(src.order_status,'')
		OR ISNULL(tgt.order_total,'') <> ISNULL(src.order_total,'')
)
THEN UPDATE SET
	tgt.order_status = src.order_status,
    tgt.order_total = src.order_total

WHEN NOT MATCHED BY TARGET THEN
INSERT (order_id,order_date, customer_id, sales_rep_id,order_status,order_total)
VALUES (src.order_id,src.order_date, src.customer_id, src.sales_rep_id,src.order_status,src.order_total);


/*======================================================
   STEP 4: VERIFY RESULTS - POST MERGE IMPLEMENTATION
===================================================== 

Select count(*) from dbo.fact_orders; --Record  Count ->  30,500 (500 New Records got inserted)

Updates Sample validation:
Select fo.* from dbo.fact_orders fo
where fo.order_id in (6000076, 6000099, 6000166) 
6000076	2023-03-20	500023	23	Returned	18968.140625
6000099	2023-12-29	500105	37	Returned	13941.599609375
6000166	2024-01-24	500063	29	Returned	71115.5234375

Order status and order total has been updated as expected for the above samples
*/