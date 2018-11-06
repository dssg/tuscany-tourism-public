import sys
sys.path.append('../src/models/geo2vec')
import json
import numpy as np
from run_single import run

# load config file
with open('config_location_clustering.json') as f:
    params = json.load(f)
    
# for season in ["summer", "post-summer", "winter"]:
    
#     params["season"] = season
    
#     for cluster in np.arange(10, 71, 5):
        
#         print("Number of clusters = ", cluster, '; Season:', season)
#         params["N_CLUSTERS"] = cluster
#         # run model
#         run(params)
run(params)