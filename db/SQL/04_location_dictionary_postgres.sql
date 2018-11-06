--- TODO: Put this after python script for creating the shapefile
--- Territories
--- The shape file for territories is manually created using the information of the communes in each territory
ogr2ogr -f "PostgreSQL" PG:'$PGCONNECTION' 
-t_srs EPSG:4326 Tus_28districts.shp -nlt PROMOTE_TO_MULTI -lco precision=NO -lco SCHEMA=tuscany


--- 	location_dictionary: This table contains the region, commune, province and territory the cell tower belongs to
--- 	We create this table on postgres and copy it to the redshift database as we cannot run spatial queries on Redshift
---     	location_id: Location ID of the cell towers in Italy
---     	region: The region code in Italy that the tower falls into
---     	province: The province code in Italy that the tower falls into (Provinces are divisions of a region)
---     	pro_com: The commune code in Italy that the tower falls into (Communes are divisions of a province)
---     	territory: The territory code in Italy that the tower falls into (Territories are the new administrative divisions of a region)
---				territories are available for the region of Tuscany
---     	cm_code: DONT KNOW WHAT THIS IS. NEED TO ADD

--- Query to create location_dictionary
create table tuscany.location_dictionary as (
	select location_id from tuscany.location
);


--- Adding all the columns
alter table tuscany.location_dictionary
add region decimal;

alter table tuscany.location_dictionary
add province decimal;

alter table tuscany.location_dictionary
add pro_com decimal;

alter table tuscany.location_dictionary
add territory decimal;

alter table tuscany.location_dictionary
add cm_code decimal;

--- creating temp table with locations and the commune they are in
create temp table locs as (
	select location_id,tpt.tuscany.com2016_wgs84_g.cod_reg as region,tpt.tuscany.com2016_wgs84_g.cod_cm as cm_code,
	tpt.tuscany.com2016_wgs84_g.cod_pro as province,tpt.tuscany.com2016_wgs84_g.pro_com,
	tpt.tuscany.com_to_district.territory 
	from tpt.tuscany.location, tpt.tuscany.com2016_wgs84_g
	left join tuscany.com_to_district on com_to_district.pro_com = tuscany.com2016_wgs84_g.pro_com
	where ST_within(tpt.tuscany.location.geom,tpt.tuscany.com2016_wgs84_g.wkb_geometry)
)

begin transaction;

--- Update the target table using an inner join with the staging table
update tuscany.location_dictionary
set region = locs.region,
	province = locs.province,
	pro_com = locs.pro_com,
	cm_code = locs.cm_code,
	territory = locs.territory
from locs
where tuscany.location_dictionary.location_id = locs.location_id;

--- End transaction and commit
end transaction;

--- Drop the staging table
drop table locs;



--- ST_within above excludes cases which are on the border for which we need to find the nearest commune as below
create temp table missing_locs as (
	with locs as (
	select location_id 
	from tuscany.location, tuscany.cmprov2016_wgs84_g
	where ST_within(geom,tuscany.cmprov2016_wgs84_g.wkb_geometry)
	),

	missing_locs as (
	select tuscany.location.location_id, tuscany.location.geom
	from tuscany.location
	where tuscany.location.location_id not in (select locs.location_id from locs)
	),

	nearest_locs as (
	select missing_locs.location_id, tuscany.com2016_wgs84_g.cod_reg,tuscany.com2016_wgs84_g.cod_cm,
	tuscany.com2016_wgs84_g.cod_pro,tuscany.com2016_wgs84_g.pro_com
	from missing_locs join tuscany.com2016_wgs84_g
	on ST_DWithin(missing_locs.geom,com2016_wgs84_g.wkb_geometry,10)
	order by missing_locs.location_id, ST_Distance(missing_locs.geom,com2016_wgs84_g.wkb_geometry)
	)

	SELECT DISTINCT ON (nearest_locs.location_id) nearest_locs.location_id,nearest_locs.cod_reg as region,nearest_locs.cod_cm as cm_code,
	nearest_locs.cod_pro as province,nearest_locs.pro_com, tuscany.com_to_district.territory
	FROM nearest_locs
	join tuscany.com_to_district on com_to_district.pro_com = nearest_locs.pro_com 
);


begin transaction;

--- Update the target table using an inner join with the staging table
update tuscany.location_dictionary
set region = missing_locs.region,
	province = missing_locs.province,
	pro_com = missing_locs.pro_com,
	cm_code = missing_locs.cm_code,
	territory = missing_locs.territory
from missing_locs
where tuscany.location_dictionary.location_id = missing_locs.location_id;

--- End transaction and commit
end transaction;

--- Drop the staging table
drop table missing_locs;

