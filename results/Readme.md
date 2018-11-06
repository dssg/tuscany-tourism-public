# Results

This folder contains the current results for the three clustering models: `geo2vec` (location clustering), `kmeans` (personas clustering), and `sequence_analysis` (sequence clustering). These results can also be visualized in the project [website](??).

All the models' results are separated into subfolders for the different countries and seasons, following the name convention `COUNTRY_SEASON` ('all' refers to all countries present in out database and season can be 'all', 'pre-summer', 'summer', 'post-summer', or 'winter'). Each subfolder contains the html interactive visualizations which are the outputs of the three pipelines. `kmeans` contains, in addition, the output description text used in the website. `sequence_analysis` contains subfolders for the visualization of the heatmaps and trajectories of each cluster (for each country/season), named `clusterwise_heatmaps` and `clusterwise_trajectories`, respectively.  
