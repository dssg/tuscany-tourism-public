# Pipeline for the models

## Location clustering

The location clustering uses the geo2vec model (see [Geo2vec](https://github.com/dssg/TPT_tourism/tree/master/src/models/geo2vec) for details) to cluster the locations visited by tourists of a given country in a given season. Broadly speaking, the model cluster municipalities that appear in the same 'context' often (i.e., are frequently visited in the same trip).

To run the model, simply type `python3 location_clustering.py` from the `pipeline` folder. The script `location_clustering.py` imports the model scripts located in `src/models/geo2vec` and perform the appropriate steps (see the model's readme file for details about each step). The input parameters for geo2vec can be chosen and modified in the configuration file `config_location_clustering.json`, located in this folder. This file contains the following parameters:

General simulation parameters:
- `username`: str, the user's username to access the Vodafone Italy database
- `season`: str, the season to be used for the location clustering. Possibilities are: 'pre-summer', 'summer', 'post-summer', 'winter', and 'all' (include all the dataset, from May/2017 to Feb/2018)
- `country`: str, the name of the country to be used. Use 'all' to include all countries for a given season.

Geo2vec internal parameters (see see [Geo2vec](https://github.com/dssg/TPT_tourism/tree/master/src/models/geo2vec) for a explanation of how each of them affect the model's results):
- `EMB_SIZE`: the dimension of the embedding array to be created by the model.
- `WINDOW_SIZE`: the window size used to train the model
- `N_EPOCHS`: number of epochs used to train the model 
- `N_CLUSTERS`: number of clusters to be used (for the whole Italy)
- `MIN_LENGTH`: minimum number of municipalities in a single trip. Tourists that visited a smaller number of municipalities are excluded from the model. Default value: 0.
- `MIN_COUNT`: minimum number of a times a single municipality has to appear in the dataset to be taken into acount during the model training. Default value: 2.

User interaction parameters:
- `train_model`: bool, if True, train the model with given parameters, if False, only initialize, but do not train, the model
- `apply_tsne`: bool, if True, include the tsne analysis at the end of the simulation. For the majority of cases this is not necessary, as it does not affect the model's results. 
- `plot_clusters_italy`: bool, if True, plot the clusters for the whole Italy
- `plot_clusters_tuscany`: bool, if True, plot the clusters for the Tuscany region

The location cluster results are stored in the folder `/results/geo2vec/` as html files, in separated subfolders for each country and season. Each subfolder contains the clustering map for Tuscany resulting from a particular set of model internal parameters (indicated in the the files' names).

## K-means 

To run k-means, see the [model description](https://github.com/dssg/TPT_tourism/blob/master/src/models/README.md). The configuration file has the following parameters:

General simulation parameters:
- `username`: str, the user's username to access the Vodafone Italy database
- `season`: str, the season to be used for the location clustering. Possibilities are: 'pre-summer', 'summer', 'post-summer', 'winter', and 'all' (include all the dataset, from May/2017 to Feb/2018)
- `country`: str, the name of the country to be used. Use 'all' to include all countries for a given season.

Model parameters:
- `nc`: int, number of clusters to divide the data
- `names`: list, list of cluster names as strings. Must be of size `nc`. Ex: ["cluster 1","cluster 2","cluster 3","cluster 4"]
- `colors`: list, list of colors to use for the clusters, in rgb format. Ex: ["rgb(255,255,0)","rgb(34,139,34)","rgb(220,20,60)","rgb(70,130,180)","rgb(128,0,128)"]

User interaction parameters:
- `mapbox_access_token`: a mapbox access token to make the plots

## Trajectory clustering

The trajectory clustering uses [partitioning about medoids](https://en.wikipedia.org/wiki/K-medoids) to find groups of tourists from a given country in a given season that follow similar trajectories. In broad terms, the model finds groups that have similar traveling behavior in Italy.

To run the model, simply type

`python3 sequence_preprocessing.py ../config_sequence_analysis.json`

`Rscript sequence_clustering.R ../config_sequence_analysis.json`

``python3 sequence_vizualization.py ../config_sequence_analysis.json``

from the `pipeline/sequence_analysis` folder. The bash script runs the `cluster_sequences.R` model located in `src/models/sequence_analysis` and perform the appropriate steps (see the model's readme file for details about each step). The input parameters for sequence analysis can be chosen and modified in the configuration file `config_sequence_analysis.json`, located in this folder. This file contains the following parameters:

General simulation parameters:
- `username`: str, the user's username to access the Vodafone Italy database
- `season`: str, the season to be used for the location clustering. Possibilities are: 'pre-summer', 'summer', 'post-summer', 'winter', and 'all' (include all the dataset, from May/2017 to Feb/2018)
- `country`: str, the name of the country to be used. Use 'all' to include all countries for a given season.

Model parameters:
- `min_trip`: int, minimum number of municipalities for a trip to be included in the clustering. Default: 0
- `max_trip`: int, maximum number of municipalities for a trip to be included in the clustering. Default: 30
- `align_by_day_of_week`: bool, if False, the sequences are not aligned based on the day of week of arrival, i.e., to capture broad patterns in trajectories irrespective of the day of arrival. Recommended: False
- `window_hrs`: int, interval at which the sequences are built, i.e., each trajectory is converted to the locations the customers were at every time interval
- `country_for_missing`: bool, if True, the country of origin is taken into account for the model; if False, the country of origin is ignored. Default: True
- `n_threads`: int, number of threads to use for the analysis
- `N_samples`: int, number of customers to sample for the clustering. Default: 40000
- `sub_cost_method`: str, method to compute substitution cost for the model. Default: "CONSTANT"
- `seq_dist_method`: str, method to compute distance between trajectories. Default: "LCS"
- `n_clusters`: int, number of clusters to classify the tourists

User interaction parameters:
- `plot_medoid_summary`: bool, if True, plot the medoid summary with the medoid trajectories for each cluster
- `plot_each_cluster`: bool, if True, plot sample trajectories for each cluster
- `n_trajectories_per_cluster`: int, number of sample trajectories to plot for each cluster
- `plot_heatmap`: bool, if True, plot the heatmaps for each cluster

The trajectory cluster results are stored in the folder `/results/sequence_analysis/` as html files, in separated subfolders for each country and season. Each subfolder contains the trajectory plots for the medoids of each cluster, examples of trajectories and heatmaps for each cluster, and the descriptive text generate from the data. The files are named based on the  model internal parameters (indicated in the the files' names).
