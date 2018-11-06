--- 	TODO: Add python script to load table from postgres and save as a csv in s3 to load into python
--- 	location_dictionary: This table contains the region, commune, province and territory the cell tower belongs to
--- 	We created this table on postgres and copy it to the redshift database as we cannot run spatial queries on Redshift
---     	location_id: Location ID of the cell towers in Italy
---     	region: The region code in Italy that the tower falls into
---     	province: The province code in Italy that the tower falls into (Provinces are divisions of a region)
---     	pro_com: The commune code in Italy that the tower falls into (Communes are divisions of a province)
---     	territory: The territory code in Italy that the tower falls into (Territories are the new administrative divisions of a region)
---				territories are available for the region of Tuscany
---     	cm_code: DONT KNOW WHAT THIS IS. NEED TO ADD


--- Create table Location dictionary table on redshift
create table tuscany.location_dictionary(
	location_id decimal,
	region decimal,
	province decimal,
	pro_com decimal,
	territory decimal,
	cm_code decimal
);

--- Code to copy data into the table created above
copy tuscany.location_dictionary 
from 's3://dssg2018-tuscany/location_dictionary.csv' 
REGION 'eu-central-1' 
iam_role 'arn:aws:iam::072669257039:role/Redshift_to_s3_Role' 
delimiter ';' IGNOREHEADER 1;

