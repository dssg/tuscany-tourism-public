--- Database: Redshift

--- Schema: Tuscany
--- Table:  Location Mapping
--- 	location_mapping: This table maps Location IDs to decimal numbers from 1 to N 
---			to save space when loading into Python dataframe
---     	location_id: Distinct location IDs from the raw data tuscany.vodafone (text)
---			location_nr: Unique integer number for each location


create table tuscany.location_mapping as (
	select location_id,
	row_number() over (partition by 1) as location_nr 
	from tuscany.location_dictionary);
	

--- temp table with mapping
create temp table loc_map as (
	select location_id,location_nr
	from tuscany.location_mapping);

-- altering location_dictionary table
alter table tuscany.location_dictionary
add location_nr decimal;

begin transaction;

-- Update the target table using an inner join with the staging table
update tuscany.location_dictionary
set location_nr = loc_map.location_nr
from loc_map
where tuscany.location_dictionary.location_id = loc_map.location_id;

-- End transaction and commit
end transaction;

-- Drop the staging table
drop table loc_map;
