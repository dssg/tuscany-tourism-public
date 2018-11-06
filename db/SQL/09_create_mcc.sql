-- Creating an MCC table which will store country and mcc code
create table tuscany.mcc(
	mcc DECIMAL,
	country TEXT 
);

--- Code to copy data into the table copy tuscany.mcc 
from 's3://dssg2018-tuscany/mcc_country.csv' 
REGION 'eu-central-1' 
iam_role 'arn:aws:iam::072669257039:role/Redshift_to_s3_Role'
delimiter ',' IGNOREHEADER 1;