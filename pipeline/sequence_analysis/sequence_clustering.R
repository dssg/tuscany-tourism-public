# Main pipeline file to run the clustering part of the sequence analysis. 
# It can be run as `Rscript sequence_clustering.R ../config_sequence_analysis.json`
# It loads the parameters from the json config file and calls the clustering function to run the analysis.

library(rjson)

source("../../src/models/sequence_analysis/cluster_sequences.R")

## accessing the config file
args = commandArgs(trailingOnly=TRUE)
params <- fromJSON(file=args[1])

seq_name <- get_seq_file_name(params)

country <- params$country
season <- params$season
N <- params$N_samples
sub_cost_method <- params$sub_cost_method 
seq_dist_method <- params$seq_dist_method
cluster_method <- params$cluster_method
n_cluster <- params$n_cluster
seed <- params$seed

## calling the main clustering function
cluster_sequences(seq_name,country,season,N,seed=seed,sub_cost_method,seq_dist_method,cluster_method,n_cluster)
