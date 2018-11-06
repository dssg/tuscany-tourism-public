# Location Clustering with embeddings

The location clustering is done with a combination of the geo2vec model and a simple clustering algorithm (k-means). The geo2vec model creates an embedding matrix based on some training data (i.e., municipalities visited by tourists during a trip that included Tuscany), which contains a vector of dimention `EMB_SIZE` for each of the municipalities in Italy. These vectors are then clustered in a given number of clusters `N_CLUSTERS`, each of these containing municipalities that are commonly visited in the same trip. The municipalities are finally plotted with a color code in a map. This approach was inspired by a previous implementation of listing embeddings for a recommendations website[1].

## Loading the data

Before applying the clustering model, data has to be preprocessed to be in the right format and filtered to include only the trips we wish to use for the clustering. This is done by the `geolocation` module (`src/utils`), which also filters the data based on the minimum number of visited municipalities in a trip (`MIN_LENGHT`). 


## Geo2vec

We use gensim's implementation of the word2vec model[2], comonly applied for natural language processing. This choice was made based on the similarity of both tasks: we want to infer which cities typically appear together in the same trip in a similar way to words appearing in the same context. The model create and train embeddings for each of the municipalities that appear in the training data, using the skip-gram algorithm[3]. 

The model needs a few hyperparameters which we tunned for our purposes (included as default values in the config files, in the `pipeline` folder). It is important to mention, however, that different sets of hyperparameters might lead to different results, and the optimal solution is still subject of ongoing research (see, for example, [4]).

## k-means for embedding clustering

After creating the embedding matrix, the clustering can be simply done by applying the k-means algorithm. It assigns clusters labels to the municipalities and allow for the plotting of the colorful and interactive Tuscany map (by importing the `viz/fancy_maps.py`). Importantly, the model's random seed (`random_state` variable) should be set in order to have replicable results. 

## Next steps

- Tune model hyperparameters
- Improve model by applying hierarchical clustering instead of simple k-means
- Optmize embedding dimension. Although `EMB_SIZE = 32` works well compared to other tested values, a systematic analysis on this parameter has not been done.

## References

[1] https://medium.com/airbnb-engineering/listing-embeddings-for-similar-listing-recommendations-and-real-time-personalization-in-search-601172f7603e

[2] https://radimrehurek.com/gensim/models/word2vec.html

[3] https://towardsdatascience.com/word2vec-skip-gram-model-part-1-intuition-78614e4d6e0b

[4] http://www.ntu.edu.sg/home/boan/papers/AAAI17_Visitor.pdf
