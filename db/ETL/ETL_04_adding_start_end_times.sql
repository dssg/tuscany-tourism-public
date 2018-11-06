--- Database: Redshift
---	Schema: Tuscany

---	Adding starting and ending times for each customer in the customer_feature and customer_arrays table
---		st_time: Time stamp of the first instance in the raw data for each customer
---		en_time: Time stamp of the last instance in the raw data for each customer

--- adding columns in the respective tables
alter table tuscany.customer_arrays
add st_time timestamp;

alter table tuscany.customer_arrays
add en_time timestamp;

alter table tuscany.customer_feature
add st_time timestamp;

alter table tuscany.customer_feature
add en_time timestamp;

create temp table st_en_times as (
	select customer_id, min(time_stamp) as st_time, max(time_stamp) as en_time
	from tuscany.vodafone
	where customer_id not in (select customer_id from tuscany.excluded_customers)
	group by customer_id
);

begin transaction;

-- Update the target table using an inner join with the staging table
update tuscany.customer_arrays
set st_time = st_en_times.st_time,
	en_time = st_en_times.en_time
from st_en_times
where tuscany.customer_arrays.customer_id = st_en_times.customer_id;

-- End transaction and commit
end transaction;

begin transaction;

-- Update the target table using an inner join with the staging table
update tuscany.customer_feature
set st_time = st_en_times.st_time,
	en_time = st_en_times.en_time
from st_en_times
where tuscany.customer_feature.customer_id = st_en_times.customer_id;

-- End transaction and commit
end transaction;

drop table st_en_times;


alter table tuscany.customer_arrays
add trip_duration decimal(4,2);

create temp table trip_dur as (
	select customer_id,datediff(hour,st_time,en_time)/CAST(24 AS Decimal(4,2)) as days
	from tuscany.customer_arrays
);

begin transaction;

update tuscany.customer_arrays
set trip_duration = trip_dur.days
from trip_dur
where trip_dur.customer_id = customer_arrays.customer_id;

end transaction;

drop table trip_dur;
