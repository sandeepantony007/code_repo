use VayuAir

/* 1 -> Loading data to Date Dimension table*/

INSERT INTO dw.DimDate
(
    date_key,
    full_date,
    day_number,
    month_number,
    month_name,
    quarter_number,
    year_number,
    day_of_week
)
SELECT DISTINCT
       CONVERT(INT,CONVERT(CHAR(8),d.dt,112)),
       d.dt,
       DAY(d.dt),
       MONTH(d.dt),
       DATENAME(MONTH,d.dt),
       DATEPART(QUARTER,d.dt),
       YEAR(d.dt),
       DATENAME(WEEKDAY,d.dt)
FROM
(
    SELECT booking_date AS dt
    FROM bronze_bookings

    UNION

    SELECT travel_date
    FROM bronze_bookings
) d
WHERE NOT EXISTS
(
    SELECT 1
    FROM dw.DimDate dd
    WHERE dd.date_key = CONVERT(INT,CONVERT(CHAR(8),d.dt,112))
);

/* 2 -> Loading data to Passenger Dimension table*/
INSERT INTO dw.DimPassenger
(
    passenger_id,
    passenger_name,
    home_airport_code,
    frequent_flyer_tier,
    signup_date
)
SELECT
    passenger_id,
    passenger_name,
    home_airport_code,
    frequent_flyer_tier,
    signup_date
FROM bronze_passengers bp
WHERE NOT EXISTS
(
    SELECT 1
    FROM dw.DimPassenger dp
    WHERE dp.passenger_id = bp.passenger_id
);

/* 3 -> Loading data to Airport Dimension table*/
INSERT INTO dw.DimAirport
(
    airport_code,
    airport_name,
    city,
    country,
    region
)
SELECT
    airport_code,
    airport_name,
    city,
    country,
    region
FROM bronze_airports ba
WHERE NOT EXISTS
(
    SELECT 1
    FROM dw.DimAirport da
    WHERE da.airport_code = ba.airport_code
);


/* 4 -> Loading data to Aircraft Dimension table*/
INSERT INTO dw.DimAircraft
(
    aircraft_code,
    model,
    manufacturer,
    seat_capacity
)
SELECT
    aircraft_code,
    model,
    manufacturer,
    seat_capacity
FROM bronze_aircraft bac
WHERE NOT EXISTS
(
    SELECT 1
    FROM dw.DimAircraft da
    WHERE da.aircraft_code = bac.aircraft_code
);

/* 5 -> Loading data to Flight Dimension table*/
INSERT INTO dw.DimFlight
(
    flight_id,
    flight_number,
    flight_date
)
SELECT
    flight_id,
    flight_number,
    flight_date
FROM bronze_flights bf
WHERE NOT EXISTS
(
    SELECT 1
    FROM dw.DimFlight df
    WHERE df.flight_id = bf.flight_id
);


/* 6 -> Loading data to FactTicketSales Fact table*/
INSERT INTO dw.FactTicketSales
(
    booking_id,
    booking_date_key,
    travel_date_key,
    passenger_key,
    flight_key,
    origin_airport_key,
    destination_airport_key,
    aircraft_key,
    fare_amount,
    tax_amount,
    miles_earned
)
SELECT

    b.booking_id,

    CONVERT(INT,CONVERT(CHAR(8),b.booking_date,112)),

    CONVERT(INT,CONVERT(CHAR(8),b.travel_date,112)),

    p.passenger_key,

    f.flight_key,

    oa.airport_key,

    da.airport_key,

    ac.aircraft_key,

    b.fare_amount,

    b.tax_amount,

    b.miles_earned

FROM bronze_bookings b

INNER JOIN dw.DimPassenger p
    ON b.passenger_id = p.passenger_id

INNER JOIN dw.DimFlight f
    ON b.flight_id = f.flight_id

INNER JOIN dbo.bronze_flights bf
    ON b.flight_id=bf.flight_id 

INNER JOIN dw.DimAirport oa
    ON bf.origin_airport_code = oa.airport_code

INNER JOIN dw.DimAirport da
    ON bf.dest_airport_code = da.airport_code

INNER JOIN dw.DimAircraft ac
    ON bf.aircraft_code = ac.aircraft_code;

/*Verifying the fact row count with bronze_bookings source table*/
    SELECT
    (SELECT COUNT(*) FROM bronze_bookings) AS BronzeBookings,
    (SELECT COUNT(*) FROM dw.FactTicketSales) AS FactRows;


/*Verifying every fact row resolves to all dimensions*/
SELECT COUNT(*) AS UnresolvedRows
FROM dw.FactTicketSales f
LEFT JOIN dw.DimDate bd
    ON f.booking_date_key = bd.date_key
LEFT JOIN dw.DimDate td
    ON f.travel_date_key = td.date_key
LEFT JOIN dw.DimPassenger p
    ON f.passenger_key = p.passenger_key
LEFT JOIN dw.DimFlight fl
    ON f.flight_key = fl.flight_key
LEFT JOIN dw.DimAirport oa
    ON f.origin_airport_key = oa.airport_key
LEFT JOIN dw.DimAirport da
    ON f.destination_airport_key = da.airport_key
LEFT JOIN dw.DimAircraft ac
    ON f.aircraft_key = ac.aircraft_key
WHERE bd.date_key IS NULL
   OR td.date_key IS NULL
   OR p.passenger_key IS NULL
   OR fl.flight_key IS NULL
   OR oa.airport_key IS NULL
   OR da.airport_key IS NULL
   OR ac.aircraft_key IS NULL;