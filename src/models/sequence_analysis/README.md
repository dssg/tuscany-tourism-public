# Sequence analysis

To cluster the tourist based on their behaviours, we use a sequence analysis approach to cluster the individual trajectories themselevs. This is an alternative approach to clustering that does not depend on extracting features but clusters the actual paths taken by the tourists directly. This analysis involves the following three steps.

- Aligning Sequences: Individual sequences need to be aligned such that they have the same time resolution and are of the same lenghts.
- Computing distance matrix: Then, using a metric to compare sequences, we can compute distances between each pair of trajectories.
- Clustering the distance matrix: Lastly, this distance matrix can be clustered using k-medoids alogorithm.

The output of this analysis is a set of medoids which are the representative individual trajectories for each cluster and a vector of clustering labels. This approach is used in the social sciences to study life-course and career trajectories of individuals. 

## Loading the data

Before applying the clustering model, data has to be preprocessed to be in the right format and filtered to include only the trips we wish to use for the clustering. This is done by the `sequence_analysis` module (`src/utils`), which filters the data based on the country and season of analysis. We can also filter based on the duration of trip if we wish to analyse short and long trips separately. 

## Sampling

As this methodology involves the construction of a distance matrix (N x N), where N is the number of individuals being analysed, it was necessary to analyse a sample of the data. We employed a sampling strategy that involved aggregating the sequences first such that each sequence has a weight based on the number of individuals with the exact same trajectory. Then, we sample 40000 trajectories (maximum possible due to computational limitations) for analysis based on these weights. With this approach, the trajectories that appear more frequently have a higher probability of being sampled for analysis. 


## Distance Matrix

The distance between trajectories is computed using a pre-defined cost and the length of the Longest Common Subsequence (LCS). Two trajectories are closer together if they have more states in the right order (not necessirily consecutive) in common. For example: The longest common subsequence between *A-A-B-C-C-D* and *A-A-A-D-D-D* is *A-D* (length 2) and therefore the distance between them is 4 x *COST*. Standard practice is to set the cost to 2 and therefore the distance between these two sequences is 8. Similarly, the costs between every pair of trajectories is computed to fill the full matrix. 

## k-medoids algorithm 

After creating the distance matrix, the clustering can be simply done by applying the k-medoids algorithm. It is an iterative algorithm that assigns cluster labels to each individual/trajectory such that the cluster quality is optimized. It assigns a medoid to every cluster (similar to a centroid in k-means algorithm) which is one individual/trajectory that is representative of that cluster.

## Next steps

This project used the simplest implementation of the approach. With more time, further improvements could be made to make it better. 

- Implement a more intelligent costing mechanism based on the distance between points
- Utilise the Optimal Matching Algorithm with above cost structure instead of the LCS metric
- Implement a clustering approach that could cluster the full data in batches/samples or solve the computational challenges in using full data through the use of High Performance Computing resources.
