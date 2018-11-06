--- Creates location_features table at Redshift


drop table if exists tuscany.location_features;

CREATE TABLE tuscany.location_features 
(
	location_id DECIMAL(20,10) NOT null,
	lat DECIMAL(20,10) NOT NULL,
	lon DECIMAL(20,10) NOT NULL,
	region DECIMAL NOT NULL,
	forest_area DECIMAL(30,20) NOT NULL,
	water_area DECIMAL(30,20) NOT NULL,
	park_area DECIMAL(30,20) NOT NULL,
	riverbank_area DECIMAL(30,20) NOT NULL,
	num_attractions DECIMAL NOT NULL,
	coast DECIMAL NOT NULL,
	arezzo DECIMAL,
	carrara DECIMAL,
	firenze DECIMAL,
	grosseto DECIMAL,
	livorno DECIMAL,
	lucca DECIMAL,
	pisa DECIMAL,
	pistoia DECIMAL,
	siena DECIMAL
	);

---How to add this part of the pipeline???

copy tuscany.location_features
from 's3://dssg2018-tuscany/location_features.csv'
REGION 'eu-central-1'
iam_role 'arn:aws:iam::072669257039:role/Redshift_to_s3_Role'
delimiter ',' IGNOREHEADER 1;