

CREATE TABLE tuscany.location_features 
(
	lat DECIMAL(8,6) NOT NULL,
	lon DECIMAL(8,6) NOT NULL,
	region DECIMAL NOT NULL,
	forest_area DECIMAL(30,20) NOT NULL,
	water_area DECIMAL(30,20) NOT NULL,
	park_area DECIMAL(30,20) NOT NULL,
	riverbank_area DECIMAL(30,20) NOT NULL,
	num_attractions DECIMAL NOT NULL,
	num_village DECIMAL NOT NULL,
	pop_village DECIMAL NOT NULL,
	pop_max_village DECIMAL NOT NULL,
	num_town DECIMAL NOT NULL,
	pop_town DECIMAL NOT NULL,
	pop_max_town DECIMAL NOT NULL,
	num_locality DECIMAL NOT NULL,
	pop_locality DECIMAL NOT NULL,
	pop_max_locality DECIMAL NOT NULL,
	num_suburb DECIMAL NOT NULL,
	pop_suburb DECIMAL NOT NULL,
	pop_max_suburb DECIMAL NOT NULL,
	num_city DECIMAL NOT NULL,
	pop_city DECIMAL NOT NULL,
	pop_max_city DECIMAL NOT NULL,
	num_island DECIMAL NOT NULL,
	num_airport DECIMAL NOT NULL,
	coast DECIMAL NOT NULL,
	arezzo DECIMAL,
	carrara DECIMAL,
	firenze DECIMAL,
	livorno DECIMAL,
	lucca DECIMAL,
	pisa DECIMAL,
	pistoia DECIMAL,
	siena DECIMAL,
	location_id DECIMAL(20,10) NOT null
	);



copy tuscany.location_features
from 's3://dssg2018-tuscany/loca_id_features2.csv'
REGION 'eu-central-1'
iam_role 'arn:aws:iam::072669257039:role/Redshift_to_s3_Role'
delimiter ',' IGNOREHEADER 1;
