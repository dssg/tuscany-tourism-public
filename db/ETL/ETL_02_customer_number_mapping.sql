--- Database: Redshift

--- Schema: Tuscany
--- Table:  Customer Mapping
--- 	customer_mapping: This table maps hashed customer IDs to decimal numbers to save space
---			when loading into Python dataframe
---     	customer_id: Distinct Customer IDs from the raw data tuscany.vodafone (text)
---			customer_nr: Unique integer number for each customer

create table tuscany.customer_mapping as (
	select customer_id,
	row_number() over (partition by 1) as customer_nr 
	from tuscany.customer_feature
);


--- Mapping Customer Number to the customer_feature table

--- temp table with mapping
create temp table cus_map as (
	select customer_id,customer_nr
	from tuscany.customer_mapping);

--- altering customer feature table
alter table tuscany.customer_feature
add customer_nr decimal;

begin transaction;

-- Update the target table using an inner join with the staging table
update tuscany.customer_feature
set customer_nr = cus_map.customer_nr
from cus_map
where tuscany.customer_feature.customer_id = cus_map.customer_id;

-- End transaction and commit
end transaction;

--- Mapping Customer Number to the customer_feature table

alter table tuscany.customer_arrays
add customer_nr decimal;

begin transaction;

-- Update the target table using an inner join with the staging table
update tuscany.customer_arrays
set customer_nr = cus_map.customer_nr
from cus_map
where tuscany.customer_arrays.customer_id = cus_map.customer_id;

-- End transaction and commit
end transaction;

-- Drop the staging table
drop table cus_map;
