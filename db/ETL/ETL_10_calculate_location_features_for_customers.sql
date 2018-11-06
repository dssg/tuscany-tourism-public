--- The below set of scripts calculate features of the locations each customer has visited and add them to the customer features table
--- Values of a given location feature is positive if a customer spent at least 20 mins in a location with the respective feature. 
--- We calcuated location features for the following groups:

---  Total time spent at all locations
--- 	total_time: Total time at all locations

---  Time spent at different landscapes:
---		forest: Number of minutes the customer spent nearby cell towers that are in or near forests
--- 	water: Number of minutes the customer nearby cell towers that are in or near water body
---  	river: Number of minutes the customer spent nearby cell towers that are near rivers
---		park: Number of minutes the customer spent nearby cell towers that are in or near parks
---		coast: Number of minutes the customer spent nearby cell towers that are along the coast


---  Time spent at cities: For this group of features, the values under each city name refers to the number of minutes a customer spent nearby cell towers in the city. These cities include: 
---     Arrezo, Florence, Grosseto, Livorno, Lucca, Pisa, Pistoia, Siena

---  Number of attractions visited
---     num_attrs: Total number of attractions visited

alter table tuscany.customer_feature
add total_time decimal;

alter table tuscany.customer_feature
add forest decimal(30,20);

alter table tuscany.customer_feature
add water decimal(30,20);

alter table tuscany.customer_feature
add river decimal(30,20);

alter table tuscany.customer_feature
add park decimal(30,20);

alter table tuscany.customer_feature
add arezzo decimal;

alter table tuscany.customer_feature
add florence decimal;

alter table tuscany.customer_feature
add grosseto decimal;

alter table tuscany.customer_feature
add livorno decimal;

alter table tuscany.customer_feature
add lucca decimal;

alter table tuscany.customer_feature
add pisa decimal;

alter table tuscany.customer_feature
add pistoia decimal;

alter table tuscany.customer_feature
add siena decimal;

alter table tuscany.customer_feature
add coast decimal;

alter table tuscany.customer_feature
add num_attrs decimal;


create temp table locs_features as (
	select 
	times.customer_id,
	sum(times.diff) as total_time,
	sum(times.diff * locs.forest_area) as forest,
	sum(times.diff * locs.water_area) as water,
	sum(times.diff * locs.riverbank_area) as river,
	sum(times.diff * locs.park_area) as park,
	sum(times.diff * locs.arezzo) as arezzo,
	sum(times.diff * locs.firenze) as florence,
	sum(times.diff * locs.grosseto) as grosseto,
	sum(times.diff * locs.livorno) as livorno,
	sum(times.diff * locs.lucca) as lucca,
	sum(times.diff * locs.pisa) as pisa,
	sum(times.diff * locs.pistoia) as pistoia,
	sum(times.diff* locs.siena) as siena,
	sum(times.diff* locs.coast) as coast,
	sum(locs.num_attractions) as num_attrs
	from tuscany.times_at_locations times
	left join tuscany.location_features as locs
	on times.location_id = locs.location_id
	where diff>20
	group by times.customer_id
);


begin transaction;

--- Update the target table using an inner join with the staging table
update tuscany.customer_feature
set total_time = locs_features.total_time,
forest = locs_features.forest,
water = locs_features.water,
river = locs_features.river,
park = locs_features.park,
arezzo = locs_features.arezzo,
florence = locs_features.florence,
grosseto = locs_features.grosseto,
livorno = locs_features.livorno,
lucca = locs_features.lucca,
pisa = locs_features.pisa,
pistoia = locs_features.pistoia,
siena = locs_features.siena,
coast = locs_features.coast,
num_attrs = locs_features.num_attrs
from locs_features
where tuscany.customer_feature.customer_id = locs_features.customer_id;

--- End transaction and commit
end transaction;

--- Drop the staging table
drop table locs_features;
