--- Database: Redshift

--- The below set of scripts create the base features for each customer and put them in the customer features table
--- These features play two key roles:
--- 	1. Filtering customers for analysis based on some of these features such as time spent
---		2. Feeding into the modeling later down in the pipeline

--- 	Table structure:
--- 	customer_feature: This table contains the features for each customer from the raw data for analysis and filtering
---     	customer_id: Distinct Customer IDs from the raw data tuscany.vodafone (text)
---     	mcc: The individual's Mobile Country Code (decimal)

---			Arrival, Times and high-level location features for Italy

---     	hrs_in_italy: The number of hours individual spent in Italy
---     	hr_arvl_italy: The hour of arrival in Italy. i.e. the hour of the first event for the customer
---     	day_of_wk_arvl_italy: The day of week of arrival in Italy. i.e. the weekday of the first event for the customer
---     	mon_arvl_italy: The month of arrival in Italy. i.e. the month of the first event for the customer
---     	day_arvl_italy: The day of arrival in Italy. i.e. the day of the first event for the customer
---     	loc_arvl_italy: The location ID of arrival in Italy. i.e. the location ID of the first event for the customer
---			num_unique_loc_in_italy: The number of unique location IDs visited in Italy
---			num_loc_in_italy: The total number of location IDs visited in Italy

---			Arrival, Times and high-level location features for Tuscany

---     	hrs_in_tusc: The number of hours individual spent in Tuscany
---     	hr_arvl_tusc: The hour of arrival in Tuscany. i.e. the hour of the first event for the customer in Tuscany
---     	day_of_wk_arvl_tusc: The day of week of arrival in Tuscany. i.e. the weekday of the first event for the customer in Tuscany
---     	mon_arvl_tusc: The month of arrival in Tuscany. i.e. the month of the first event for the customer in Tuscany
---     	day_arvl_tusc: The day of arrival in Tuscany. i.e. the day of the first event for the customer in Tuscany
---     	loc_arvl_tusc: The location ID of arrival in Tuscany. i.e. the location ID of the first event for the customer in Tuscany
---			num_unique_loc_in_tusc: The number of unique location IDs visited in Tuscany
---			num_loc_in_tusc: The total number of location IDs visited in Tuscany

---			Times and high-level location features outside Tuscany from the above set of features

---     	hrs_outside_tuscany: The number of hours individual spent outside Tuscany
---			locs_outside_tuscany: The number of locations an individual visited outside Tuscany
---			unique_locs_outside_tuscany: The number of unique locations visited outside Tuscany


--- Creating customer feature table
create table tuscany.customer_feature as (select distinct customer_id from tuscany.vodafone);

--- Adding empty feature column MCC
alter table tuscany.customer_feature
add mcc decimal;

--- Creating a temporary table for extracting the MCC and dumping into the table
create temp table cus_mcc as
select distinct customer_id, mcc
from tuscany.vodafone
group by customer_id;

begin transaction;

--- Update the target table using an inner join with the staging table
update tuscany.customer_feature
set mcc = cus_mcc.mcc
from cus_mcc
where tuscany.customer_feature.customer_id = cus_mcc.customer_id
;

--- End transaction and commit
end transaction;

--- Drop the staging table
drop table cus_mcc;


---	Arrival and time spent in Italy features
	
--- adding italy arrival features
alter table tuscany.customer_feature
add hrs_in_italy decimal(8,2);

alter table tuscany.customer_feature
add hr_arvl_italy decimal;

alter table tuscany.customer_feature
add day_of_wk_arvl_italy decimal;

alter table tuscany.customer_feature
add mon_arvl_italy decimal;

alter table tuscany.customer_feature
add day_arvl_italy decimal;
	
alter table tuscany.customer_feature
add loc_arvl_italy decimal;


--- creating temporary table with the feature queries for arrival in italy
create temp table italy_features as (
	with italy_loc as (
		select distinct customer_id, first_value(location_id) 
		over (partition by customer_id order by time_stamp asc rows between unbounded preceding and unbounded following) 
		as loc_arvl_italy
		from tuscany.vodafone
		)
	select v.customer_id, 
		datediff(minutes, min(time_stamp), max(time_stamp))/60 as hrs_in_italy,
		extract(hr from min(time_stamp)) as hr_arvl_italy,
		extract(dayofweek from min(time_stamp)) as day_of_wk_arvl_italy,
		extract(mon from min(time_stamp)) as mon_arvl_italy,
		extract(d from min(time_stamp)) as day_arvl_italy,
		il.loc_arvl_italy
	from tuscany.vodafone as v
	left join italy_loc as il on v.customer_id = il.customer_id
	group by v.customer_id, il.loc_arvl_italy);

begin transaction;

--- Update the target table using an inner join with the staging table
update tuscany.customer_feature
set hrs_in_italy = italy_features.hrs_in_italy,
hr_arvl_italy = italy_features.hr_arvl_italy,
day_of_wk_arvl_italy = italy_features.day_of_wk_arvl_italy,
mon_arvl_italy = italy_features.mon_arvl_italy,
day_arvl_italy = italy_features.day_arvl_italy,
loc_arvl_italy = italy_features.loc_arvl_italy
from italy_features
where tuscany.customer_feature.customer_id = italy_features.customer_id;

--- End transaction and commit
end transaction;

--- Drop the staging table
drop table italy_features;

---	Features for locations visited in Italy

alter table tuscany.customer_feature
add num_unique_loc_in_italy decimal;

alter table tuscany.customer_feature
add num_loc_in_italy decimal;

--- number of locations in italy, number of unique locations in italy
create temp table locs_it_features as (
select 
	customer_id,
	count(distinct location_id) as num_unique_loc_in_italy,
	count(location_id) as num_loc_in_italy
from tpt.tuscany.vodafone
group by customer_id);

begin transaction;

--- Update the target table using an inner join with the staging table
update tuscany.customer_feature
set num_unique_loc_in_italy = locs_it_features.num_unique_loc_in_italy,
num_loc_in_italy = locs_it_features.num_loc_in_italy
from locs_it_features
where tuscany.customer_feature.customer_id = locs_it_features.customer_id;

--- End transaction and commit
end transaction;

--- Drop the staging table
drop table locs_it_features;

---	Features for locations visited in Tuscany

alter table tuscany.customer_feature
add num_unique_loc_in_tusc decimal;

alter table tuscany.customer_feature
add num_loc_in_tusc decimal;


--- number of locations in tuscany, number of unique locations in tuscany

create temp table locs_tusc_features as (
select 
	customer_id,
	count(distinct vod.location_id) as num_unique_loc_in_tusc,
	count(vod.location_id) as num_loc_in_tusc
from tpt.tuscany.vodafone vod
inner join tpt.tuscany.location_dictionary locs
on locs.location_id=vod.location_id
where locs.region = '9'
group by customer_id);


begin transaction;

--- Update the target table using an inner join with the staging table
update tuscany.customer_feature
set num_unique_loc_in_tusc = locs_tusc_features.num_unique_loc_in_tusc,
num_loc_in_tusc = locs_tusc_features.num_loc_in_tusc
from locs_tusc_features
where tuscany.customer_feature.customer_id = locs_tusc_features.customer_id;

--- End transaction and commit
end transaction;

--- Drop the staging table
drop table locs_tusc_features;


---	Feature of time spent in Tuscany
alter table tuscany.customer_feature
add hrs_in_tusc decimal(8,2);


create temp table time_in_tusc as (
	with customer_regions as (
		select customer_id, time_stamp, tuscany.location_dictionary.region as rgn
		from tuscany.vodafone
		join tuscany.location_dictionary on location_dictionary.location_id = vodafone.location_id
		order by customer_id,time_stamp
	), 

	region_chunks as (
		select customer_regions.customer_id, time_stamp, lead(time_stamp,1) over 
		(partition by customer_id order by time_stamp asc) as t2
		from customer_regions
		where customer_regions.rgn = 9
		order by time_stamp asc
	)

	select region_chunks.customer_id, sum(datediff(minutes,time_stamp,t2))/60 as hrs_in_tusc
	from region_chunks
	where t2 is not null
	group by customer_id);


begin transaction;

--- Update the target table using an inner join with the staging table
update tuscany.customer_feature
set hrs_in_tusc = time_in_tusc.hrs_in_tusc
from time_in_tusc
where tuscany.customer_feature.customer_id = time_in_tusc.customer_id;

--- End transaction and commit
end transaction;

--- Drop the staging table
drop table time_in_tusc;


---	Arrival and time spent in Tuscany features
alter table tuscany.customer_feature
add hr_arvl_tusc decimal;

alter table tuscany.customer_feature
add day_of_wk_arvl_tusc decimal;

alter table tuscany.customer_feature
add mon_arvl_tusc decimal;

alter table tuscany.customer_feature
add day_arvl_tusc decimal;

alter table tuscany.customer_feature
add loc_arvl_tusc decimal;


create temp table tusc_features as (
with tusc as (
	select customer_id, time_stamp, l.location_id from tuscany.vodafone 
	join tuscany.location_dictionary as l on 
	l.location_id=vodafone.location_id
	where l.region=9
	),
	tusc_loc as (
	select distinct customer_id, first_value(location_id) 
	over (partition by customer_id order by time_stamp asc rows between unbounded preceding and unbounded following) 
	as loc_arvl_tusc
	from tusc
	)
select t.customer_id, 
	extract(hr from min(time_stamp)) as hr_arvl_tusc,
	extract(dayofweek from min(time_stamp)) as day_of_wk_arvl_tusc,
	extract(mon from min(time_stamp)) as mon_arvl_tusc,
	extract(d from min(time_stamp)) as day_arvl_tusc,
	tl.loc_arvl_tusc
	from tusc as t
left join tusc_loc as tl on t.customer_id = tl.customer_id
group by t.customer_id, --t.hr_arvl_tusc, t.day_of_wk_arvl_tusc, t.mon_arvl_tusc, t.day_arvl_tusc,
		tl.loc_arvl_tusc);

begin transaction;

--- Update the target table using an inner join with the staging table
update tuscany.customer_feature
set hr_arvl_tusc = tusc_features.hr_arvl_tusc,
day_of_wk_arvl_tusc = tusc_features.day_of_wk_arvl_tusc,
mon_arvl_tusc = tusc_features.mon_arvl_tusc,
day_arvl_tusc = tusc_features.day_arvl_tusc,
loc_arvl_tusc = tusc_features.loc_arvl_tusc
from tusc_features
where tuscany.customer_feature.customer_id = tusc_features.customer_id;

--- End transaction and commit
end transaction;

--- Drop the staging table
drop table tusc_features;


---	Times and high-level location features outside Tuscany from the above set of features

--- adding hrs outside tuscany
alter table tuscany.customer_feature
add hrs_outside_tuscany decimal(8,2);

update tuscany.customer_feature
set hrs_outside_tuscany = (hrs_in_italy - hrs_in_tusc);

--- adding locations outside tuscany
alter table tuscany.customer_feature
add locs_outside_tuscany decimal;

update tuscany.customer_feature
set locs_outside_tuscany = (num_loc_in_italy - num_loc_in_tusc);

--- adding unique locations outside tuscany
alter table tuscany.customer_feature
add unique_locs_outside_tuscany decimal;

update tuscany.customer_feature
set unique_locs_outside_tuscany = (num_unique_loc_in_italy - num_unique_loc_in_tusc);


