"""
File that runs the preprocessing part of the pipeline.
When passed along with the config file such as `python3 sequence_preprocessing.py ../config_sequence_analysis.json`,
it will pick up the parameters from the config file and pass onto the relevant functions to plot the results of the analysis. 
"""

import os
import sys
import json

r_path = "../../src/utils/"
sys.path.append(r_path)

from sequence_analysis import sequence_preprocessing as sf

config_path = sys.argv[1]

# load config file
with open(config_path) as f:
    params = json.load(f)

seq_path,clus_res_path,clus_res_name = sf.create_paths(params)

username = params["username"]
season = params["season"]
country = params["country"]
min_trip = params["min_trip"]
max_trip = params["max_trip"]
align_by_day_of_week = params["align_by_day_of_week"]
window_hrs = params["window_hrs"]
country_for_missing = params["country_for_missing"]
n_threads = params["n_threads"]

## calling the main pre-processing function
sf.preprocess_sequences(username, season, country, min_trip, max_trip, align_by_day_of_week, window_hrs, country_for_missing, seq_path, n_threads)
