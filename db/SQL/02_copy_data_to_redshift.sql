--- Script to copy raw data into Redshift Table from the S3 directory
--- To copy data into redshift, the raw data must rest in a csv or a gzip file on a S3 bucket
--- In our case the directory on s3 is dssg2018-tuscany. Make sure to change it to reflect your directory


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
	CUSTOMER_ID TEXT ,
	MCC DECIMAL,
	TIME_STAMP TIMESTAMP,
	LOCATION_ID DECIMAL 
);

--- Code to copy data into the table created above (May-July)
copy tuscany.vodafone 
from 's3://dssg2018-tuscany/dssg_2018_May_July.csv.gz' 
REGION 'eu-central-1' 
iam_role 'arn:aws:iam::072669257039:role/Redshift_to_s3_Role' 
delimiter ',' timeformat 'DD-MON-YY HH24:MI:SS' gzip;

--- Code to copy data into the table created above (Aug-Oct)
copy tuscany.vodafone 
from 's3://dssg2018-tuscany/dssg_2018_Aug_Oct.csv.gz' 
REGION 'eu-central-1' 
iam_role 'arn:aws:iam::072669257039:role/Redshift_to_s3_Role' 
delimiter ',' timeformat 'DD-MON-YY HH24:MI:SS' gzip;

--- Code to copy data into the table created above (Nov-Feb)
copy tuscany.vodafone 
from 's3://dssg2018-tuscany/dssg_2018_Nov_Feb.csv.gz' 
REGION 'eu-central-1' 
iam_role 'arn:aws:iam::072669257039:role/Redshift_to_s3_Role' 
delimiter ',' timeformat 'DD-MON-YY HH24:MI:SS' gzip;



--- 	location: This table contains the location details (latitude and longitude) of the cell towers
---     	location_id: Location ID of the cell towers in Italy
---     	lat: latitude of the cell tower
---     	lon: longitude of the cell tower

--- Code to create table in the scheme
CREATE TABLE tuscany.location(
	LOCATION_ID DECIMAL NOT NULL, 
	LAT float NOT NULL, 
	LON float NOT null
);

--- Code to copy data into the table created above
copy tuscany.location 
from 's3://dssg2018-tuscany/dssg_2018_location_lookup.csv' 
REGION 'eu-central-1' 
iam_role 'arn:aws:iam::072669257039:role/Redshift_to_s3_Role' 
delimiter ',' IGNOREHEADER 1;


