library(rjson)

source("../../src/models/sequence_analysis/cluster_sequences.R")

args = commandArgs(trailingOnly=TRUE)
params <- fromJSON(file=args[1])

seq_name <- get_seq_file_name(params)

country <- params$country
season <- params$season
N <- params$N_samples
sub_cost_method <- params$sub_cost_method 
seq_dist_method <- params$seq_dist_method 
n_cluster <- params$n_cluster
seed <- params$seed

print(paste0(country,"_",season))

k_range <- c(2:10)
find_optimal_clusters(seq_name,country,season,N,seed=seed,sub_cost_method,seq_dist_method,k_range)
