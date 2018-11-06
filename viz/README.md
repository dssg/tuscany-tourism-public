# Visualizations

Scripts for the visualizations of the models' results. 

`maps.py` contains the the Map class, which plots non-interactive visualizations using [matplotlib](https://matplotlib.org/).

`fancy_maps.py` contains the fancier, interactive plots and uses [bokeh](https://bokeh.pydata.org/en/latest/docs/reference/models/mappers.html). This script is used for generating interactive html plots from custom shapefiles containing the municipalities in Tuscany, and is imported in the pipelines of the geo2vec and sequence_analysis models.

`comune_centroids.csv` contains a pandas DataFrame with the centroid latitude and longitude for the municipalities in Tuscany.
