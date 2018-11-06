# Models

## K-means
Our persona analysis groups tourists based on their interests, such as which cities and attractions they visited in Tuscany. We clustered tourists in the pre-summer and summer season based on time-space and behavioural features, using k-means clustering, Our optimal solution revelaed 4 clusters in both cases. 

### How to run it?

1) Import the description library, which imports the clustering library too
```python
import sys
r_path_data = "../src/utils/descriptive_engine/"
sys.path.append(r_path_data)
from descriptives import *
```

1) Import the library:
```python
import sys
sys.path.append("..")
from connect_db import db_connection
```

2) Import config file:
```python
"""
CONFIG FILE EXAMPLE:
{"username": "YOURNAME",
 "season": "winter",
 "country": "United States",
 "nc":4,
"names": ["cluster 1","cluster 2","cluster 3","cluster 4"],
"colors": ["rgb(255,255,0)","rgb(34,139,34)","rgb(220,20,60)","rgb(70,130,180)","rgb(128,0,128)"],
"mapbox_access_token":"YOUR MAPBOX TOKEN"}
""""
import json

with open('../pipeline/config_json') as f:
    params = json.load(f)
    
username = params["username"]
season = params["season"]
country = params["country"]
nc = params["nc"]
names = params["names"]
colors = params["colors"]
mapbox_access_token = params["mapbox_access_token"]

```

3) Now, you are ready run the clustering

```python
"""
Returns unscaled features with cluster labels based on k-means

Parameters:
username: Username to access data via get_k_means_data
season: Season to be chosen to perform analyses - 'pre-summer', 'summer', 'post-summer', 'winter', or 'all' for the whole year
country: Country to be chosen to perform analyses, if country='all', runs on the full data
features: a dictionary with keys equal to the arguments of the function, values list of df variables (defoult)
hrs: If True, choose feature group that contains hours spent in Tuscany, hours spent outside Tuscany
numlocs: If True, choose feature group that contains number of locations and number of unique locations visited in Tuscany and Italy
location: If True, choose feature group that contains time spent (in mumtiples of ) at the locations with respective features, including landscape, cities visited, and total number of attactions visited.
latlon: If True, choose feature group that contains latitude and longitude of average location, most visited location, start and end location, and standard deviation of all lat/lon
nc: Number of clusters to be used in k-means
write: If True, write k-means results (features dataframe with cluster labels) to csv file
path: path to save csv file
outfile: filename of csv file
"""

result=get_cluster_results(username,season, country, features, nc)

```

4) Generate interactive visualizations

```python
"""
Creates and interactive html output of the clusters, if the number of points is more 100K randomly sample 50K of them
    
Parameters:
result: Dataframe, constaining  k-means clustering results under the column 'label'
names: List of cluster names in order
country: Country to be chosen to perform analyses, if country='all', runs on the full data
season: Season to be chosen to perform analyses - 'pre-summer', 'summer', 'post-summer', 'winter', or 'all' for the whole year
mapbox_access_token: your mapbox access token, create here: https://www.mapbox.com/help/how-access-tokens-work/
    
Returns an html file saved to .../results/kmeans/country_season/country_season.html
"""

f=plot_kmeans(result1, names, colors, country, season, mapbox_access_token)
```
5) Generate description

```python
"""
Prints out description for clusters

Parameters:
result: clustering result with customer features
season: names of the season used for clustering
country: name of the country (all=all country)
var: 'label': k-means results
     'cluster': trajectory results
n: number of nationalities lsited in description, if country=='all'
names: cluster names

Returns an txt file saved to .../results/kmeans/country_season/country_season.html
"""

get_kmeans_description(result1, season, country, var, nc, n, names)
```

## Sequence analysis

Trajectory analysis finds the most frequent paths among tourists. We clustered a set of different nationalities in different seasons purely based on tourists’ individual spatial trajectories or sequences categorised by location  (eg: Florence -> Pisa -> Livorno ) We used optimal matching to to compute distances between sequences (cost of insertion, deletion and substitution to match two sequences) and the resulting distance matrix was clustered by the k-medoids algorithm. This clustering methodology takes into account timing (e.g: When does a tourist visit Florence), Duration (e.g: How long does a tourist stay in Florence) and order (e.g: Where did they come from and where do they go next) to create the clusters of trajectories. 

### How to run it?



## Geo2Vec

Location clustering shows which municipalities in the region are visited together during the same trip. The location clustering is done with a combination of the geo2vec model and the k-means clustering algorithm. The geo2vec model creates an embedding matrix based on some training data (in our case, ordered sequences of municipalities visited by tourists during a trip that included Tuscany), which contains a vector of a given dimension for each of the municipalities in Italy. These vectors are then clustered in a given number of clusters. Each of these clusters contain municipalities that are commonly visited in the same trip. This approach was inspired by a previous implementation of listing embeddings for a recommendations website, and relies on the implementation of a famous natural language processing algorithm, [word2vec](https://en.wikipedia.org/wiki/Word2vec). 

### How to run it?

#### Example
The model can be run once by executing the `run_single.py` script (alternatively, you can run `location_clustering.py` in the `pipeline` folder). The script does the following:

1) Loads the parameters from a given config file

2) Load the preprocessing module and preprocess/filter the data
```python
"""
Parameters:
season: names of the season used for clustering
country: name of the country (all=all countries)
MIN_LENGHT: minimum number of municipalities in a single trip

Returns an txt file saved to .../results/kmeans/country_season/country_season.html
"""

sys.path.append("../src/utils/geolocation/")
import preprocessing

if country == 'all':
    df_trips = load_df.get_geo2vec_data_all_country(username, season).rename(columns={'com_locs_trunc':'locations'})
else:
    df_trips = load_df.get_geo2vec_data(username, season, country).rename(columns={'com_locs_trunc':'locations'})
        
preprocessing.str_to_list(df_trips)
df_trips_red = preprocessing.filter_short_trips(df_trips, min_length=MIN_LENGTH)
```

3) Load shape files

```python
sys.path.append("../src/utils/")
from load_data import load_dataframes as load_df

path_shapefiles, regions, provinces, territories, municipalities, crs = read_files.read_shapefile_data(path_to_shapefiles, 'shape_files_path.json')
df_mun_tus = read_files.read_shapefiles_in(True, path_shapefiles, municipalities, crs)
```
4) Initialize and run the geo2vec model

```python

 g2v = Geo2vec(EMB_SIZE, WINDOW_SIZE, season, country)
 # initialize model
 g2v.initialize(sequences=df_trips_red['locations_list'], min_count=MIN_COUNT)
 # train model
 if train_model:       
     g2v.train(df_trips_red['locations_list'], n_epochs=N_EPOCHS)
```

5) Do the clustering

```python
 # cluster model
 g2v.create_clusters(n_clusters=N_CLUSTERS)
```

6) Plot the clusters in the Tuscany map

```python
if plot_clusters_tuscany:
    print('\nTUSCANY -- plotting...\n\n')
    g2v.merge_gdf(df_mun_tus)
    g2v.get_most_similar()
    g2v.pickle_cluster_labels(tag='Tuscany')   
    plt_loc(g2v.gdf_clusters,
            path_to_file=path_to_final_plots+'{}_{}/'.format(country, season),
            file_name='Location_cluster_Tuscany_EMB{}_WIN{}_EPO{}_CLU{}_MinL{}_MinC{}.html'.format(EMB_SIZE, WINDOW_SIZE, N_EPOCHS, N_CLUSTERS, MIN_LENGTH, MIN_COUNT))
```
