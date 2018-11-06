
alter table tuscany.edgelist_comune_italy
add weight_filtered_time1day decimal default 0;


create temp table filtered_el as (
	WITH addloc AS
	(
	select
	        vod.customer_id,
	        vod.time_stamp,
	        vod.l1 as pro_com
	from tpt.tuscany.customer_loc_times vod
	where vod.diff > 24*60
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
set weight_filtered_time1day = filtered_el.weight
from filtered_el
where tuscany.edgelist_comune_italy.pro_com = filtered_el.pro_com
and tuscany.edgelist_comune_italy.new_pro_com = filtered_el.new_pro_com;

-- End transaction and commit
end transaction;

-- Drop the staging table
drop table filtered_el;
