--- Script to copy raw data into Postgres Table from the directory
--- Move the open a postgres session in the directory where the raw data files are

--- Schema: Tuscany

--- Tables
--- 	vodafone: Table containing the IP Probe data from Vodafone for May 2017 to Feb 2018
---     The data contains events of the SIM connecting to the nearest cell tower at 1 minute intervals    
---     	customer_id: Hashed customer ID in the raw data (Character)
---     	MCC: Mobile Country Code of the SIM (Decimal)
---     	time_stamp: timestamp of the event connecting to cell tower (timestamp)
---     	location_id: Location ID of the nearest cell tower (Decimal)


--- Code to create table in the scheme
create table tuscany.vodafone(
	CUSTOMER_ID VARCHAR NOT NULL, 
	MCC DECIMAL, 
	TIME_STAMP timestamp NOT NULL, 
	LOCATION_ID DECIMAL NOT NULL
);

--- Code to copy data into the table created above
\COPY tuscany.vodafone from 'dssg_2018_May_July.csv' (delimiter',');
\COPY tuscany.vodafone from 'dssg_2018_Aug_Oct.csv' (delimiter',');
\COPY tuscany.vodafone from 'dssg_2018_Nov_Feb.csv' (delimiter',');


--- 	location: This table contains the location details (latitude and longitude) of the cell towers
---     	location_id: Location ID of the cell towers in Italy
---     	lat: latitude of the cell tower
---     	lon: longitude of the cell tower

--- Code to create table in the scheme
CREATE TABLE tuscany.location(
	LOCATION_ID DECIMAL NOT NULL, 
	LAT DECIMAL NOT NULL, 
	LON DECIMAL NOT null
);

--- Code to copy data into the table created above
\COPY tuscany.location from 'dssg_2018_location_lookup.csv' WITH CSV HEADER;

--- Creating a PostGIS column to use the latitude and longitude information and make it a geom point field
--- This would allow us to perform spatial queries using PostGIS features
ALTER TABLE tuscany.location ADD COLUMN geom geometry(Point,4326);
SELECT ST_SetSRID(ST_MakePoint(lon, lat),4326) as geom from tuscany.location;


--- Loading Shapefiles into Postgres
--- The shapefiles of the different divisions of Italy into Regions, Provinces, Communes and Ambiti territoriali are as below

--- Regions

ogr2ogr -f "PostgreSQL" PG:'$PGCONNECTION'
-t_srs EPSG:4326 Reg_2016_WGS84_g.shp -nlt PROMOTE_TO_MULTI -lco precision=NO -lco SCHEMA=tuscany


--- Provinces

ogr2ogr -f "PostgreSQL" PG:'$PGCONNECTION'
-t_srs EPSG:4326 CMprov2016_WGS84_g.shp -nlt PROMOTE_TO_MULTI -lco precision=NO -lco SCHEMA=tuscany

--- Comunes

ogr2ogr -f "PostgreSQL" PG:'$PGCONNECTION'
-t_srs EPSG:4326 Com2016_WGS84_g.shp -nlt PROMOTE_TO_MULTI -lco precision=NO -lco SCHEMA=tuscany





