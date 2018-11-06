import sys
r_path_data = "../src/utils/descriptive_engine/"
sys.path.append(r_path_data)
from descriptives import *

import json

# load config file
with open('config_location_k_means.json') as f:
    params = json.load(f)
    
username = params["username"]
season = params["season"]
country = params["country"]
nc = params["nc"]
names = params["names"]
colors = params["colors"]
mapbox_access_token = params["mapbox_access_token"]


# run model and save results
result = get_cluster_results(username,season, country, features, nc)
plot_kmeans(result, names, colors, country, season, mapbox_access_token)
get_kmeans_description(result, season, country, "label")
