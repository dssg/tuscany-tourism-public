drop table tuscany.german_august_locs_features

create table tuscany.german_august_locs_features as 
(
with cus_loc as ( 
		select customer_id,time_stamp, location_id,lead(location_id,1) over (partition by customer_id order by time_stamp asc) as l2 
		from tuscany.german_august
		order by customer_id, time_stamp asc
	),

dist_loc_times as (
		select customer_id, time_stamp,location_id,l2
		from cus_loc
		where location_id != l2 or l2 is null
	),

lag_times as (
		select customer_id,time_stamp,location_id, lead(time_stamp,1) over 
				(partition by customer_id order by time_stamp asc) as t2
		from dist_loc_times
		order by time_stamp asc
	),

create_time_diff as (
	select customer_id,time_stamp,location_id,datediff(minutes,time_stamp,t2) as diff
	from lag_times
	order by customer_id,time_stamp
	)

select 
times.customer_id,
sum(times.diff) as total_time,
sum(times.diff * locs.forest_area) as forest,
sum(times.diff * locs.water_area) as water,
sum(times.diff * locs.riverbank_area) as river,
sum(times.diff * locs.park_area) as park,
sum(times.diff * locs.arezzo) as arezzo,
sum(times.diff * locs.firenze) as florence,
sum(times.diff * locs.livorno) as livorno,
sum(times.diff * locs.lucca) as lucca,
sum(times.diff * locs.pisa) as pisa,
sum(times.diff * locs.pistoia) as pistoia,
sum(times.diff* locs.siena) as siena,
sum(times.diff* locs.coast) as coast,
sum(locs.num_attractions) as num_attrs,
sum(locs.num_town) as towns,
sum(times.diff * locs.num_island) as islands,
sum(times.diff * locs.num_suburb) as subrub
from  create_time_diff times
left join tuscany.location_features as locs
on times.location_id = locs.location_id
where diff>20
group by times.customer_id
);