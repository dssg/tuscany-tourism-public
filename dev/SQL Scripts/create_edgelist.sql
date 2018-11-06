create table tuscany.edgelist_comune_italy(
	pro_com decimal,
	new_pro_com decimal,
	weight decimal
);

insert into tuscany.edgelist_comune_italy (

	WITH addloc AS
	(
	select
	        vod.customer_id,
	        vod.time_stamp,
	        locs.pro_com
	from tpt.tuscany.vodafone vod
	left join
	(select location_id, pro_com,region from tpt.tuscany.location_dictionary) locs
	on locs.location_id=vod.location_id
	),

	edgelist AS
	(
	select pro_com,
	 LAG (pro_com,1) OVER (partition by customer_id ORDER BY time_stamp) AS new_pro_com
	FROM addloc)

	select pro_com, new_pro_com, count(*) as weight
	from edgelist
	GROUP BY pro_com, new_pro_com

);


delete from tuscany.edgelist_comune_italy
where pro_com is null or new_pro_com is null;


alter table tuscany.edgelist_comune_italy
add weight_filtered decimal default 0;


create temp table filtered_el as (
	WITH addloc AS
	(
	select
	        vod.customer_id,
	        vod.time_stamp,
	        locs.pro_com
	from tpt.tuscany.vodafone vod
	left join
	(select location_id, pro_com,region from tpt.tuscany.location_dictionary) locs
	on locs.location_id=vod.location_id
	where vod.customer_id not in (select customer_id from tuscany.excluded_customers)
	),

	edgelist AS
	(
	select pro_com,
	 LAG (pro_com,1) OVER (partition by customer_id ORDER BY time_stamp) AS new_pro_com
	FROM addloc)

	select pro_com, new_pro_com, count(*) as weight
	from edgelist
	GROUP BY pro_com, new_pro_com

);


begin transaction;

-- Update the target table using an inner join with the staging table
update tuscany.edgelist_comune_italy
set weight_filtered = filtered_el.weight
from filtered_el
where tuscany.edgelist_comune_italy.pro_com = filtered_el.pro_com
and tuscany.edgelist_comune_italy.new_pro_com = filtered_el.new_pro_com;

-- End transaction and commit
end transaction;

-- Drop the staging table
drop table time_in_tusc;



