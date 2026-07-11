

/* Creating Country dimension from Airport*/

CREATE TABLE dw.DimCountry
(
    country_key INT IDENTITY(1,1) PRIMARY KEY,
    country_name VARCHAR(100) NOT NULL UNIQUE,
    region VARCHAR(100)
);

/*Creating City Dimension table from Airport and country dimension*/

CREATE TABLE dw.DimCity
(
    city_key INT IDENTITY(1,1) PRIMARY KEY,
    city_name VARCHAR(100) NOT NULL,
    country_key INT NOT NULL,

    CONSTRAINT FK_DimCity_DimCountry
        FOREIGN KEY (country_key)
        REFERENCES dw.DimCountry(country_key)
);


/*load City Dimension*/
INSERT INTO dw.DimCountry (country_name, region)
SELECT DISTINCT
       country,
       region
FROM bronze_airports;

/*load city Dimesion*/
INSERT INTO dw.DimCity (city_name, country_key)
SELECT DISTINCT
       ba.city,
       dc.country_key
FROM bronze_airports ba
JOIN dw.DimCountry dc
    ON ba.country = dc.country_name;

/*Modifying DimAirport*/
ALTER TABLE dw.DimAirport
ADD city_key INT;
GO

Select * from dw.DimAirport;

UPDATE a
SET a.city_key = c.city_key
FROM dw.DimAirport a
JOIN bronze_airports ba
    ON a.airport_code = ba.airport_code
JOIN dw.DimCountry co
    ON ba.country = co.country_name
JOIN dw.DimCity c
    ON ba.city = c.city_name
   AND c.country_key = co.country_key;
GO

/*Updating city_key as FK in Airport Dimension table*/
ALTER TABLE dw.DimAirport
ADD CONSTRAINT FK_DimAirport_DimCity
FOREIGN KEY (city_key)
REFERENCES dw.DimCity(city_key);

/*Dropping the city and country redundat columns in Airport table*/
ALTER TABLE dw.DimAirport
DROP COLUMN city,
            country,
            region;
GO

/*Verifying all three tables Airport, country, city are linked*/
SELECT
    a.airport_code,
    a.airport_name,
    c.city_name,
    co.country_name,
    co.region
FROM dw.DimAirport a
JOIN dw.DimCity c
    ON a.city_key = c.city_key
JOIN dw.DimCountry co
    ON c.country_key = co.country_key;
GO