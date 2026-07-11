-- Drop tables in dependency order
DROP TABLE IF EXISTS dw.FactTicketSales;
GO

DROP TABLE IF EXISTS dw.DimDate;
GO

DROP TABLE IF EXISTS dw.DimPassenger;
GO

DROP TABLE IF EXISTS dw.DimFlight;
GO

DROP TABLE IF EXISTS dw.DimAirport;
GO

DROP TABLE IF EXISTS dw.DimAircraft;
GO

-- (Optional 	but safe) drop schema if you want a clean rebuild
 DROP SCHEMA IF EXISTS dw;
 GO

CREATE SCHEMA dw;
GO

CREATE TABLE dw.DimDate
(
    date_key INT PRIMARY KEY,            -- YYYYMMDD
    full_date DATE NOT NULL,
    day_number TINYINT,
    month_number TINYINT,
    month_name VARCHAR(20),
    quarter_number TINYINT,
    year_number SMALLINT,
    day_of_week VARCHAR(15)
);

CREATE TABLE dw.DimPassenger
(
    passenger_key INT IDENTITY(1,1) PRIMARY KEY,
    passenger_id INT NOT NULL UNIQUE,          -- Business Key
    passenger_name VARCHAR(100),
    home_airport_code CHAR(3),
    frequent_flyer_tier VARCHAR(20),
    signup_date DATE
);


CREATE TABLE dw.DimAirport
(
    airport_key INT IDENTITY(1,1) PRIMARY KEY,
    airport_code CHAR(3) NOT NULL UNIQUE,      -- Business Key
    airport_name VARCHAR(100),
    city VARCHAR(100),
    country VARCHAR(100),
    region VARCHAR(100)
);

CREATE TABLE dw.DimAircraft
(
    aircraft_key INT IDENTITY(1,1) PRIMARY KEY,
    aircraft_code VARCHAR(20) NOT NULL UNIQUE, -- Business Key
    model VARCHAR(100),
    manufacturer VARCHAR(50),
    seat_capacity INT
);

CREATE TABLE dw.DimFlight
(
    flight_key INT IDENTITY(1,1) PRIMARY KEY,
    flight_id INT NOT NULL UNIQUE,              -- Business Key
    flight_number VARCHAR(20),
    flight_date DATE
);


CREATE TABLE dw.FactTicketSales
(
    booking_id INT PRIMARY KEY,             -- Degenerate Dimension

    booking_date_key INT NOT NULL,
    travel_date_key INT NOT NULL,

    passenger_key INT NOT NULL,
    flight_key INT NOT NULL,

    origin_airport_key INT NOT NULL,
    destination_airport_key INT NOT NULL,

    aircraft_key INT NOT NULL,

    fare_amount DECIMAL(10,2),
    tax_amount DECIMAL(10,2),
    miles_earned INT,

    CONSTRAINT FK_Fact_BookingDate
        FOREIGN KEY (booking_date_key)
        REFERENCES dw.DimDate(date_key),

    CONSTRAINT FK_Fact_TravelDate
        FOREIGN KEY (travel_date_key)
        REFERENCES dw.DimDate(date_key),

    CONSTRAINT FK_Fact_Passenger
        FOREIGN KEY (passenger_key)
        REFERENCES dw.DimPassenger(passenger_key),

    CONSTRAINT FK_Fact_Flight
        FOREIGN KEY (flight_key)
        REFERENCES dw.DimFlight(flight_key),

    CONSTRAINT FK_Fact_OriginAirport
        FOREIGN KEY (origin_airport_key)
        REFERENCES dw.DimAirport(airport_key),

    CONSTRAINT FK_Fact_DestinationAirport
        FOREIGN KEY (destination_airport_key)
        REFERENCES dw.DimAirport(airport_key),

    CONSTRAINT FK_Fact_Aircraft
        FOREIGN KEY (aircraft_key)
        REFERENCES dw.DimAircraft(aircraft_key)
);