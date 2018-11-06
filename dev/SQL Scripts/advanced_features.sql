


-- add to full table - top/avg/std

alter table tuscany.customer_feature
drop avg_lat;
alter table tuscany.customer_feature
drop avg_lon;
alter table tuscany.customer_feature
drop top_lat;
alter table tuscany.customer_feature
drop top_lon;
alter table tuscany.customer_feature
drop std_lat;
alter table tuscany.customer_feature
drop std_lon;

alter table tuscany.customer_feature
add avg_lat decimal(8,6);
alter table tuscany.customer_feature
add avg_lon decimal(8,6);
alter table tuscany.customer_feature
add top_lat decimal(8,6);
alter table tuscany.customer_feature
add top_lon decimal(8,6);
alter table tuscany.customer_feature
add std_lat decimal(8,6);
alter table tuscany.customer_feature
add std_lon decimal(8,6);

create temp table avg_locs as (
  with lag_times as ( 
        select customer_id,loc.lat,loc.lon,loc.location_id, vodafone.time_stamp,
        lead(time_stamp,1) over (partition by customer_id order by time_stamp) as t2 
        from tuscany.vodafone
        join tuscany.location as loc on vodafone.location_id = loc.location_id 
        where customer_id not in (select customer_id from tuscany.excluded_customers)
    ),
    time_diffs as (
        select customer_id,time_stamp, t2, lat,lon, datediff(minute,time_stamp,t2) as time_diff
        from lag_times
        where t2 is not null
        order by time_stamp
    ),
    time_uniqueloc_dup as (
        select customer_id, time_stamp, lat, lon, sum(time_diff) over (partition by customer_id, lat, lon) as total_minutes,
        sum(time_diff) over (partition by customer_id) as total_minutes_italy
        from time_diffs
    ),
   time_uniqueloc as (
        select distinct customer_id, lat, lon, total_minutes, total_minutes_italy,
        first_value(lat) over (partition by customer_id order by total_minutes desc rows between unbounded preceding and unbounded following) as top_lat,
        first_value(lon) over (partition by customer_id order by total_minutes desc rows between unbounded preceding and unbounded following) as top_lon,
        stddev_samp(lat) over (partition by customer_id ) as std_lat,
        stddev_samp(lon) over (partition by customer_id ) as std_lon
        from time_uniqueloc_dup
    )
    select customer_id, top_lat, top_lon, std_lat, std_lon, sum(lat*total_minutes/total_minutes_italy) as avg_lat, sum(lon*total_minutes/total_minutes_italy) as avg_lon
    from time_uniqueloc where total_minutes_italy>0 group by customer_id, top_lat, top_lon, std_lat, std_lon
);

begin transaction;

-- Update the target table using an inner join with the staging table
update tuscany.customer_feature
set avg_lat = avg_locs.avg_lat,
    avg_lon = avg_locs.avg_lon,
    top_lat = avg_locs.top_lat,
    top_lon = avg_locs.top_lon,
    std_lat = avg_locs.std_lat,
    std_lon = avg_locs.std_lon
from avg_locs
where tuscany.customer_feature.customer_id = avg_locs.customer_id;

-- End transaction and commit
end transaction;

drop table avg_locs;




-- add start/end to full table

alter table tuscany.customer_feature
drop start_lat;
alter table tuscany.customer_feature
drop start_lon;
alter table tuscany.customer_feature
drop end_lat;
alter table tuscany.customer_feature
drop end_lon;


alter table tuscany.customer_feature
add start_lat decimal(8,6);
alter table tuscany.customer_feature
add start_lon decimal(8,6);
alter table tuscany.customer_feature
add end_lat decimal(8,6);
alter table tuscany.customer_feature
add end_lon decimal(8,6);

create temp table end_locs as (
    with lag_times as ( 
        select customer_id,loc.lat,loc.lon,loc.location_id, vodafone.time_stamp
        from tuscany.vodafone
        join tuscany.location as loc on vodafone.location_id = loc.location_id 
        where customer_id not in (select customer_id from tuscany.excluded_customers)
    )
    select distinct customer_id, 
    first_value(lat) over (partition by customer_id order by time_stamp asc rows between unbounded preceding and unbounded following) as start_lat,
    last_value(lat) over (partition by customer_id order by time_stamp asc rows between unbounded preceding and unbounded following) as end_lat,
    first_value(lon) over (partition by customer_id order by time_stamp asc rows between unbounded preceding and unbounded following) as start_lon,
    last_value(lon) over (partition by customer_id order by time_stamp asc rows between unbounded preceding and unbounded following) as end_lon    
    from lag_times
);

begin transaction;

-- Update the target table using an inner join with the staging table
update tuscany.customer_feature
set start_lat = end_locs.start_lat,
    start_lon = end_locs.start_lon,
    end_lat = end_locs.end_lat,
    end_lon = end_locs.end_lon
from end_locs
where tuscany.customer_feature.customer_id = end_locs.customer_id;

-- End transaction and commit
end transaction;

drop table end_locs;

