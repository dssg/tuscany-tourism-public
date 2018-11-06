# SQL, python and bash scripts to build database


## Data dictionaries

To run the model, the database must have the following format. The primary (raw) data is the database from Vodafone Italy, and the secondary data is the transformed and organized data the models receive as input. The tables must contain the fields:

#### Primary (raw) data

##### 1) Vodafone - Table containing the IP Probe data from Vodafone for May 2017 to Feb 2018. The data contains events of the SIM connecting to the nearest cell tower at 1 minute intervals.
- Columns:
	- customer_id: Hashed customer ID in the raw data (Character)
	- MCC: Mobile Country Code of the SIM (Decimal)
	- time_stamp: timestamp of the event connecting to cell tower (timestamp)
	- location_id: Location ID of the nearest cell tower (Decimal)
	

#### Secondary data 

##### 1) Customer_array - This table stores the sequence of municipalities visited by the individual in an array form for sequence analysis in the Pipeline. This ETL takes the raw data and creates a sequence of distinct municipalities visited and the time spent at each of these. This is then transformed into an array structure and stored in the customer_arrays table. 
- Columns:
	- customer_id: Distinct Customer IDs from the raw data tuscany.vodafone (text)
	- mcc: Mobile country code of each of the customers.
	- com_locs: array of municipalities in order of visiting by the respective customer
	- com_locs_trunc: array of municipalities in order of visiting but where at least 1 hr spent at each of them.
	- times: The time spent in minutes at each of these municpalities.

Note: Length of times array is one less than the com_locs array as we only store the differences to save space We do this instead of storing timestamps as for some cases, the length of the array exceeds the maximum size of the field. We can always recover the timestamps from the starting time_stamp and the time differences

##### 2) Customer_features - This table contains the features for each customer from the raw data for analysis and filtering
- Columns:
	- customer_id: Distinct Customer IDs from the raw data tuscany.vodafone (text)
	- mcc: The individual's Mobile Country Code (decimal)
	- hrs_in_italy: The number of hours individual spent in Italy
	- hr_arvl_italy: The hour of arrival in Italy. i.e. the hour of the first event for the customer
	- day_of_wk_arvl_italy: The day of week of arrival in Italy. i.e. the weekday of the first event for the customer
	- mon_arvl_italy: The month of arrival in Italy. i.e. the month of the first event for the customer
	- day_arvl_italy: The day of arrival in Italy. i.e. the day of the first event for the customer
	- loc_arvl_italy: The location ID of arrival in Italy. i.e. the location ID of the first event for the customer
	- num_unique_loc_in_italy: The number of unique location IDs visited in Italy
	- num_loc_in_italy: The total number of location IDs visited in Italy
	- hrs_in_tusc: The number of hours individual spent in Tuscany
	- hr_arvl_tusc: The hour of arrival in Tuscany. i.e. the hour of the first event for the customer in Tuscany
	- day_of_wk_arvl_tusc: The day of week of arrival in Tuscany. i.e. the weekday of the first event for the customer in Tuscany
	- mon_arvl_tusc: The month of arrival in Tuscany. i.e. the month of the first event for the customer in Tuscany
	- day_arvl_tusc: The day of arrival in Tuscany. i.e. the day of the first event for the customer in Tuscany
	- loc_arvl_tusc: The location ID of arrival in Tuscany. i.e. the location ID of the first event for the customer in Tuscany
	- num_unique_loc_in_tusc: The number of unique location IDs visited in Tuscany
	- num_loc_in_tusc: The total number of location IDs visited in Tuscany
	- hrs_outside_tuscany: The number of hours individual spent outside Tuscany
	- locs_outside_tuscany: The number of locations an individual visited outside Tuscany
	- unique_locs_outside_tuscany: The number of unique locations visited outside Tuscany
	- avg_lat: Average of the latitudes of all towers each customer was connected to, weighted by duration of connection
	- avg_lon: Average of the longitudes of all towers each customer was connected to, weighted by duration of connection
	- top_lat: Latitude of the tower to which each customer is connected for the longest time
	- top_lon: Longitude of the tower to which each customer is connected for the longest time
	- std_lat: Standard deviation of the latitudes of all towers each customer was connected to
	- std_lon: Standard deviation of the longitudes of all towers each customer was connected to
	- start_lat: Latitude of the tower to which each customer is connected for the first instance
	- start_lon: Longitude of the tower to which each customer is connected for the first instance
	- end_lat: Latitude of the tower to which each customer is connected for the last instance
	- end_lon: Longitude of the tower to which each customer is connected for the last instance
	- total_time: Total time at all locations
	- forest: Number of minutes the customer spent nearby cell towers that are in or near forests
	- water: Number of minutes the customer nearby cell towers that are in or near water body
	- river: Number of minutes the customer spent nearby cell towers that are near rivers
	- park: Number of minutes the customer spent nearby cell towers that are in or near parks
	- coast: Number of minutes the customer spent nearby cell towers that are along the coast
	- Time spent at cities: For this group of features, the values under each city name refers to the number of minutes a customer spent nearby cell towers in the city. These cities include: Arrezo, Florence, Grosseto, Livorno, Lucca, Pisa, Pistoia, Siena
	- num_attrs: Total number of attractions visited

##### 3) Location_dictionary - This table contains the region, commune, province and territory the cell tower belongs to. We create this table on postgres and copy it to the redshift database as we cannot run spatial queries on Redshift
- Columns:
	- location_id: Location ID of the cell towers in Italy
 	- region: The region code in Italy that the tower falls into
	- province: The province code in Italy that the tower falls into (Provinces are divisions of a region)
	- pro_com: The commune code in Italy that the tower falls into (Communes are divisions of a province)
	- territory: The territory code in Italy that the tower falls into (Territories are the new administrative divisions of a region)
	
## Data filtering

Before using the dataset, we ran basic cleaning operations to remove possibly mislabeled data, eventual mistakes, or data entries that are not relevant for the models. The steps for cleaning the data were:

#### 1) Static and Port transits
- Identifying customers spending less than 1 hr in Italy or Tuscany
- Eliminating people tranisiting at airports/ports. 
- Identifying of customers present in only 1 location in Italy or Tuscany
- Since this is a mobility study, we do not retail individuals who do not move.

#### 2) Transit through Tuscany 
- Identifying customers transiting through Tuscany
- People spending less than 1 day in Tuscany and also not in one location for more than an hour
- Tuscany being a central region of Italy has people potentially moving from the North to the South or vice versa

#### 3) Pseudo-locals
- Identifying customers spending over 30 days in the region
- These would probably be business / student exchanges in any case is a small population under the hypothesis that their behavious is different. 

#### 4) TODOs 
- A small number of entries are physically impossible (such as a single customer appearing in locations very far from each other in a very short period of time)
- 12% of the customers have at least two entries in a different location at the same time stamp. The cause should be further investigated in the dataset
	

## ETL

ETL contains all sql scripts to create intermediate databse structure on our  AWS redshift server. They need to be run in order to build the database structure needed for further analysis.

- ETL_01_customer_arrays.sql
- ETL_02_customer_number_mapping.sql
- ETL_03_location_number.sql
- ETL_04_adding_start_end_times.sql
- ETL_05_adding_lat_lon.sql


## Location features

Python and SQL code to create a feature table for tower locations.

- location_voronois.py: calculate a voronoi dhape around each tower (lot, lan)
- parse_xmls_point_of_interests.py : parse xml files contains points of interests (touristic attractions in Tuscany), given by our partner
- geographic_features_for_locations.py (calcualtes wether a vornoi contains water, forest, national park, rivers, tourist attractions)
- create_location_features_table.sql : query to create the table on Redshift

``` PostgreSQL
	location_id DECIMAL(20,10) NOT null,
	lat DECIMAL(20,10) NOT NULL,
	lon DECIMAL(20,10) NOT NULL,
	region DECIMAL NOT NULL,
	forest_area DECIMAL(30,20) NOT NULL,
	water_area DECIMAL(30,20) NOT NULL,
	park_area DECIMAL(30,20) NOT NULL,
	riverbank_area DECIMAL(30,20) NOT NULL,
	num_attractions DECIMAL NOT NULL,
	coast DECIMAL NOT NULL,
	arezzo DECIMAL,
	carrara DECIMAL,
	firenze DECIMAL,
	grosseto DECIMAL,
	livorno DECIMAL,
	lucca DECIMAL,
	pisa DECIMAL,
	pistoia DECIMAL,
	siena DECIMAL
```
    
## SQL

SQL scripts to create final database on AWS Redshift server. Code needs to be ran in order. CSV files are needed to create tables.

- 01_copy_data_to_postgres.sql
- 02_copy_data_to_redshift.sql
- 04_location_dictionary_postgres.sql
- 05_location_dictionary_to_csv.py
- 06_location_dictionary_redhsift.sql
- 07_base_feature_queries.sql
- 07_combine_comunes_to_territory.py
- 09_combine_comunes_to_territory.py
- 10_create_mcc.sql
- 11_calculate_location_features_for_customers.sql
- comuni2district.csv
- mcc_country.csv
