--- Database: Redshift
--- Schema: Tuscany

--- Table: Customer_Arrays
---		customer_arrays: This table stores the sequence of municipalities visited by the individual
---			in an array form for sequence analysis in the Pipeline. This ETL takes the raw data
---			and creates a sequence of distinct municipalities visited and the time spent at each of these.
---			This is then transformed into an array structure and stored in the customer_arrays table. 

---     	customer_id: Distinct Customer IDs from the raw data tuscany.vodafone (text)
---			mcc: Mobile country code of each of the customers.
---			com_locs: array of municipalities in order of visiting by the respective customer
---			com_locs_trunc: array of municipalities in order of visiting but where at least 1 hr spent at each of them.
---			times: The time spent in minutes at each of these municpalities.

---			Note: Length of times array is one less than the com_locs array as we only store the differences to save space
---			We do this instead of storing timestamps as for some cases, the length of the array exceeds the maximum size of the field. 
---			We can always recover the timestamps from the starting time_stamp and the time differences

create table tuscany.customer_arrays(
	customer_id varchar(max),
	mcc decimal
);

create table tuscany.customer_arrays as (
	select customer_id,mcc
	from tuscany.customer_feature
	where customer_id not in (select customer_id from tuscany.excluded_customers)
);

--- adding columns for each of the fields
alter table tuscany.customer_arrays
add com_locs varchar(max);

alter table tuscany.customer_arrays
add times varchar(max);

alter table tuscany.customer_arrays
add com_locs_trunc varchar(max);
	

create temp table com_array as (
	with cus_com as (
		select customer_id,time_stamp,loc.pro_com
		from tuscany.vodafone
		join tuscany.location_dictionary loc on loc.location_id = vodafone.location_id
		where customer_id not in (select customer_id from tuscany.excluded_customers)
	),

	cus_loc as ( 
		select customer_id,time_stamp,pro_com l1,lead(pro_com,1) over (partition by customer_id order by time_stamp asc) as l2 
		from cus_com
		order by time_stamp asc
	),

	dist_loc_times as (
		select customer_id, time_stamp,l1
		from cus_loc
		where l1 != l2 or l2 is null
	),

	lag_times as (
		select customer_id,time_stamp,l1, lead(time_stamp,1) over 
				(partition by customer_id order by time_stamp asc) as t2
		from dist_loc_times
		order by time_stamp asc
	)

	select customer_id,time_stamp,l1,datediff(minutes,time_stamp,t2) as diff
	from lag_times
	order by time_stamp
);

--- creating the location arrays
create temp table loc_array as (
	with trunc_loc as (
		select customer_id, l1, time_stamp
		from com_array
		where diff > 0 or diff is null
	)

	select customer_id,
	listagg(l1, ', ') within group (order by time_stamp) as coms_new
	from trunc_loc
	group by customer_id
);

begin transaction;

-- Update the target table using an inner join with the staging table
update tuscany.customer_arrays
set com_locs = loc_array.coms_new
from loc_array
where tuscany.customer_arrays.customer_id = loc_array.customer_id;

-- End transaction and commit
end transaction;

drop table loc_array;

--- creating the time diff arrays
create temp table time_array as (
	with trunc_loc as (
		select customer_id, l1, time_stamp,diff
		from com_array
		where diff is not null or diff > 0
	)

	select customer_id,
	listagg(diff, ', ') within group (order by time_stamp) as times
	from trunc_loc
	group by customer_id
);

begin transaction;

-- Update the target table using an inner join with the staging table
update tuscany.customer_arrays
set times = time_array.times
from time_array
where tuscany.customer_arrays.customer_id = time_array.customer_id;

-- End transaction and commit
end transaction;

drop table time_array;

--- creating the truncated location arrays
create temp table trunc_array as (
	with trunc_loc as (
		select customer_id, l1, time_stamp
		from com_array
		where diff is not null or diff >= 60
	)

	select customer_id,
	listagg(l1, ', ') within group (order by time_stamp) as coms_trunc
	from trunc_loc
	group by customer_id
);

begin transaction;

-- Update the target table using an inner join with the staging table
update tuscany.customer_arrays
set com_locs_trunc = trunc_array.coms_trunc
from trunc_array
where tuscany.customer_arrays.customer_id = trunc_array.customer_id;

-- End transaction and commit
end transaction;

drop table trunc_array;


--- Table: Customer Loc times
---		customer_loc_times: This table stores the municipalities visited and the time spent at each of these for every customer
---     	customer_id: Distinct Customer IDs from the raw data tuscany.vodafone (text)
---			l1: The commune visited by the customer
---			time_stamp: The timestamp of entry into the respective commune
---			diff: The time spent at the commune

--- This table is added as a table in the schema as a backup if we want to change the duration, etc. 

create table tuscany.customer_loc_times as (
	select * from com_array
);

drop table com_array;



