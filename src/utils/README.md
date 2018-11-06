# Utils

Utils contains all modules which helps to process data for the main models.

- `connect_db`: a module to connect to the AWS Redshift database

- `descriptive_engine`: generates text automatically based on clustering results (for sequence_analysis and k-means)

- `geolocation`: preprocessing functions for the geo2vec model

- `load_data`: send queries to `db` and return a specific dataframe for each clustering model (sequence_analysis, k-means, and geo2vec)

- `read_shapefiles`: helper module to easily read shapefiles (for Tuscany and Italy)

- `sequence_analysis`:  contains the preprocessing functions for the sequence clustering input and the trajectory visualizations

- `trajectory_descr`: create description for medoids and for each cluster (sequence analysis) and save them into a given folder as text files 
