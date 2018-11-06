# K-means module


## kmeans.py

Contains the code to run k-means clustering:

```python
get_cluster_results(username, season, country, features, nc,
                        hrs=True, numlocs=True, location=True, latlon=True,
                        write=False, path="", outfile="")
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
```

## create_interactive_chart.py

Creates interactive visulaization of cluster results on the map of Tuscany with plotly.

Note: mapbox access token is needed to draw on a map
Returns an html file saved to .../results/kmeans/country_season/country_season.html

```python
plot_kmeans(result ,names, colors, country, season, mapbox_access_token)
    """
    Creates and interactive html output of the clusters, if the number of points is more 100K randomly sample 50K of them
    result: Dataframe, constaining  k-means clustering results under the column 'label'
    names: List of cluster names in order
    country: Country to be chosen to perform analyses, if country='all', runs on the full data
    season: Season to be chosen to perform analyses - 'pre-summer', 'summer', 'post-summer', 'winter', or 'all' for the whole year
    mapbox_access_token: your mapbox access token, create here: https://www.mapbox.com/help/how-access-tokens-work/
    """
```

## plot_clusters_save_fig.py

Creates static visualization of cluster results on the map of Tuscany with plotly.
This module highly depends on read_shapefiles, and the viz/maps module

1) Import dependencies
```python
import sys
import os
sys.path.append("../src/utils/")
from read_shapefiles import read_files

import sys
r_path_data1 = "../viz/"
sys.path.append(r_path_data1)
from maps import Featuresmap

```
2) Run the visualization function

It visualizes and save the cluster result on the map of Tuscany
Returns an html file saved to .../results/kmeans/country_season/country_season.png

```python
plot_clusters(country, result, season, df_reg_tus)
```
