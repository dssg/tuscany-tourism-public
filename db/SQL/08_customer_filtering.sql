--- Database: Redshift

--- SQL Script to filter out customers for the analysis
--- We create a new table called excluded customers which has all the customer ids 
--- of the customers to be ignored for the analysis. 

--- creating the table
create table tuscany.excluded_customers(
	customer_id text
);


--- Step 1: Static and Port transits
--- 	Identifying customers spending less than 1 hr in Italy or Tuscany
---			Eliminating people tranisiting at airports/ports. 
--- 	Identifying of customers present in only 1 location in Italy or Tuscany
---			Since this is a mobility study, we do not retail individuals who do not move.

insert into tuscany.excluded_customers(select customer_id 
from tuscany.customer_feature
where hrs_in_italy < 1 or hrs_in_tusc < 1 
or num_loc_in_italy < 2 or num_loc_in_tusc < 2
or num_uniuqe_loc_in_italy < 2 or num_uniuqe_loc_in_tusc < 2
);


--- Step 2: Transit through Tuscany 
--- 	Identifying customers transiting through Tuscany
---			People spending less than 1 day in Tuscany and also not in one location for more than an hour
---			Tuscany being a central region of Italy has people potentially moving from the North to the South or vice versa

insert into tuscany.excluded_customers (
with loc_times as (
	select tuscany.vodafone.customer_id,  vodafone.location_id, loc.region, time_stamp, lag(time_stamp,1) 
	over (partition by customer_id order by time_stamp asc) as t2
	from tuscany.vodafone
    inner join tuscany.location_dictionary loc on loc.location_id = vodafone.location_id
    where customer_id in (select customer_id from tuscany.customer_feature where hrs_in_tusc < 25)
    and customer_id not in (select customer_id from tuscany.excluded_customers)
    order by time_stamp asc  
),


tusc_loc_times as (select customer_id,loc_times.location_id, region,datediff(minutes,t2,time_stamp) as mins_at_loc
from loc_times
where t2 is not null and region = 9
),

max_at_tusc_loc as (
	select customer_id,max(mins_at_loc) as max_time_tusc_loc from tusc_loc_times
	group by customer_id
)

select customer_id from max_at_tusc_loc
where max_time_tusc_loc <= 60
);


--- Step 3: pseudo-locals
--- 	Identifying customers spending over 30 days in the region
---			These would probably be business / student exchanges in any case is a small population
---			under the hypothesis that their behavious is different.  

insert into tuscany.excluded_customers (select customer_id 
	from tuscany.customer_feature
	where  hrs_in_tusc > 30*24
	and customer_id not in (select customer_id from tuscany.excluded_customers)
);

