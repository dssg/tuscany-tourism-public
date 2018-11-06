create table tuscany.german_august as (
select 
arrs.customer_id,
arrs.location_id,
arrs.time_stamp
from tpt.tuscany.vodafone as arrs
inner join 
(select customer_id , mon_arvl_tusc, mcc
from tpt.tuscany.customer_feature fe
where fe.mon_arvl_tusc = 8
and mcc = 262
and fe.customer_id not in (select customer_id from tuscany.excluded_customers)) germans
on germans.customer_id= arrs.customer_id
order by customer_id, time_stamp);
