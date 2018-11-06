"""
File that runs the visualization part of the pipeline.
When passed along with the config file such as `python3 sequence_vizualization.py ../config_sequence_analysis.json`,
it will pick up the parameters from the config file and pass onto the relevant functions to plot the results of the analysis. 
"""

import os
import sys
import json

r_path = "../../src/utils/"
sys.path.append(r_path)

from sequence_analysis import sequence_preprocessing as sf,visualize_sequences as vs
from trajectory_descr import trajectory_vis

## accessing the config file
config_path = sys.argv[1]

# load config file
with open(config_path) as f:
    params = json.load(f)

username = params["username"]
season = params["season"]
country = params["country"]
min_trip = params["min_trip"]
max_trip = params["max_trip"]

seq_path,clus_res_path,clus_res_name = sf.create_paths(params)

plot_medoid_summary = params["plot_medoid_summary"]
plot_each_cluster = params["plot_each_cluster"]
n_trajectories_per_cluster = params["n_trajectories_per_cluster"]
plot_heatmap = params["plot_heatmap"]
cluster_names = params["cluster_names"]

## calling function to add locations list to cluster results
vs.add_sequence_to_clusters(clus_res_path,clus_res_name,username, season, country, min_trip, max_trip)



# old plots
# vs.plot_clusters(clus_res_path,clus_res_name,plot_medoid_summary,plot_each_cluster,n_trajectories_per_cluster,plot_heatmap)

## calling function to plot trajectories
vs.plot_interactive_trajectories(clus_res_path,clus_res_name,cluster_names,country,plot_medoid_summary,plot_each_cluster,n_trajectories_per_cluster)

## calling function to plot heatmaps
vs.plot_cluster_heatmaps(clus_res_path,clus_res_name)

## calling function create descriptives 
trajectory_vis.trajectory_description(clus_res_path, clus_res_name, country, season, cluster_names, username)

