# """
# This R script contains the following functions relating to Sequence clustering.
# -- Create TraMineR sequence object from sequences csv
# -- Create Substitution cost matrix
# -- Compute distance between sequences
# -- Save sequence distance matrix
# -- Find optimal number of clusters
# -- Cluster sequences
# -- Save clustering results (cluster labels and medoids)
# """

suppressMessages(library(cluster))
suppressMessages(library(lattice))
suppressMessages(library(TraMineR))
suppressMessages(library(TraMineRextras))
suppressMessages(library(WeightedCluster))
suppressMessages(library(fpc))
suppressMessages(library(foreach))
suppressMessages(library(parallel))
suppressMessages(library(doParallel))
suppressMessages(library(doFuture))
suppressMessages(library(rjson))


cluster_sequences <- function(seq_name,country,season,N=20000,seed=1729,sub_cost_method="CONSTANT",seq_dist_method="LCS",cluster_method="PAM",n_cluster){
    
    # Master function to read csv file of aligned sequences, create sequence object, compute distance matrix and cluster them
    # Parameters:
    #   seq_file: path to aligned sequence
    #   N: sample size to analyse
    #   seed: random seed for sampling
    #   sub_cost_method: substirution cost method
    #   seq_dist_method: method for computing sequence distances
    #   n_cluster: number of clusters to compute

    # Returns:
    #   Saves the sequence distances and clustering results in the model path

    ## Create sequence object
    seq_dir <- paste0('../src/models/sequence_analysis/trained_models/',country,'_',season,'/sequences/')
    seq_path <- paste0(seq_dir,seq_name,".csv")
    seq_obj <- create_sequence_object(seq_path,N,seed)
    seq_weights <- attr(seq_obj,"weights")
    ## Create substitution cost matrix
    seq_subcost <- create_substitution_cost(seq_obj,method=sub_cost_method,cval=2)

    ## Load distance matrix
    seq_dist_dir <- paste0('../src/models/sequence_analysis/trained_models/',country,'_',season,'/sequence_distances/')
    seq_dist_name <- paste0(gsub("sequence","sequence_distances",seq_name),'_N_',N,'_',sub_cost_method,'_',seq_dist_method)
    seq_dist_path <- paste0(seq_dist_dir,seq_dist_name)
    if(!file.exists(paste0(seq_dist_path,".RSav"))){
        seq_dist <- compute_sequence_distances(seq_obj,seq_subcost,method=seq_dist_method)    
        ## Save distance matrix
        save_sequence_distances(seq_dist,seq_dist_path)
    }else{
        print("Loading seq dist file")
        load(file=paste0(seq_dist_path,".RSav"))
    }
    
    ## Cluster sequences
    clusters <- pam_clustering(seq_dist,seq_weights,n_cluster,cluster_method)
    
    ## Create and save clustering results
    clus_res_dir <- paste0('../results/sequence_analysis/',country,'_',season,'/')
    clus_res_name <- paste0(gsub("sequence_distances","cluster_results",seq_dist_name),'_',cluster_method,'_NClus_',n_cluster)
    clus_res_path <- paste0(clus_res_dir,clus_res_name)
    save_cluster_results(seq_obj,seq_dist,clusters,clus_res_path,cluster_method)
}


find_optimal_clusters <- function(seq_name,country,season,N=20000,seed=1729,sub_cost_method="CONSTANT",seq_dist_method="LCS",k_range){
    ## Create sequence object
    seq_dir <- paste0('../src/models/sequence_analysis/trained_models/',country,'_',season,'/sequences/')
    seq_path <- paste0(seq_dir,seq_name,".csv")
    seq_obj <- create_sequence_object(seq_path,N,seed)
    seq_weights <- attr(seq_obj,"weights")

    ## Load distance matrix
    seq_dist_dir <- paste0('../src/models/sequence_analysis/trained_models/',country,'_',season,'/sequence_distances/')
    seq_dist_name <- paste0(gsub("sequence","sequence_distances",seq_name),'_N_',N,'_',sub_cost_method,'_',seq_dist_method)
    seq_dist_path <- paste0(seq_dist_dir,seq_dist_name)
    if(!file.exists(paste0(seq_dist_path,".RSav"))){
        ## Create substitution cost matrix
        seq_subcost <- create_substitution_cost(seq_obj,method=sub_cost_method,cval=2)
        seq_dist <- compute_sequence_distances(seq_obj,seq_subcost,method=seq_dist_method)    
        ## Save distance matrix
        save_sequence_distances(seq_dist,seq_dist_path)
    }else{
        print("Loading seq dist file")
        load(file=paste0(seq_dist_path,".RSav"))
    }

    cluster_stats <- evaluate_cluster_stats(seq_dist,seq_weights,k_range)
    df_statstics <- cluster_stats$stats
    clus_stats_name <- paste0(gsub("sequence_distances","cluster_stats",seq_dist_name),'_',sub_cost_method,'_',seq_dist_method,'_k_',min(k_range),'_to_',max(k_range))
    write.csv(df_statstics,file=paste0(seq_dist_dir,clus_stats_name,".csv"))
    jpeg(paste0(seq_dist_dir,'/cluster_statistics_wcKM_ASW_CH.jpg'))
    par(mfrow=c(1:2))
    plot(x=k_range,y=df_statstics$ASW,type='l',col=2,main="ASW")
    plot(x=k_range,y=df_statstics$CH,type='l',col=2,main="CH")
    dev.off()
}

create_sequence_object <- function(seq_path,N,seed=1729){
    
    # Create a TraMineR sequence object from csv file with alinged sequences

    # Parameters:
    # model_name: file name of the sequence csv to pick up
    # N: number of seqeunces
    # seed: seed for random sampling

    # Returns:
    # seq_object: A TraMineR sequence object with unique sequences and respective weights 
    set.seed(seed)
    df_sequence <- read.csv(seq_path)
    ids <- df_sequence[,1]
    agg_seq <- wcAggregateCases(df_sequence[,-1])
    samp_size <- min(N,length(agg_seq$aggIndex))
    seq_index <- sample(agg_seq$aggIndex,size=samp_size,replace=FALSE,prob=agg_seq$aggWeights)
    unique_seq <- df_sequence[seq_index, -1]
    seq_weights <- agg_seq$aggWeights[which(agg_seq$aggIndex %in% seq_index)]
    seq_object <- seqdef(unique_seq, weights = seq_weights,id = ids[seq_index])
    return (seq_object)
}

create_substitution_cost <- function(seq_object,method="CONSTANT",cval=2){

    # Create a substitution cost martix for computing distances between sequences

    # Parameters:
    # seq_object: the TraMineR sequence object
    # method: method for computing the substitution cost
        # CONSTANT: constant cost of cval
        # TRATE: using transistion rates from the data to compute costs (refer TraMineR documentation for formulation)

    # Returns:
    # seq_subcost: A TraMineR substitution cost object
    #   $sm : has the substitution cost matrix
    #   $indel : has the insertion and deletion costs

    seq_subcost <- seqcost(seq_object,method=method,cval=cval,weighted=FALSE)
    return (seq_subcost)
}

compute_sequence_distances <- function(seq_object,seq_subcost,method="LCS"){

    # Create a substitution cost martix for computing distances between sequences

    # Parameters:
    # seq_object: the TraMineR sequence object
    # seq_subcost: the substitution cost object
        # CONSTANT: constant cost of cval
        # TRATE: using transistion rates from the data to compute costs (refer TraMineR documentation for formulation)

    # Returns:
    # seq_distances: A lower triangular matrix with distances between sequences 

    seq_distances <- seqdist(seq_object,method = method,sm=seq_subcost$sm,full.matrix=FALSE)
    return (seq_distances)
}

save_sequence_distances <- function(seq_dist,seq_dist_path){
    # Save the distance matrix between sequences

    # Parameters:
    # seq_dist: the distance matrix
    # model_name: name of the file
    
    save(seq_dist, file=paste0(seq_dist_path,".RSav"))
}


# get_pam_cluster_stats <- function(dist_matrix,k){
#     cl <- pam(dist_matrix,k=k,diss=TRUE)
#     cs <- cluster.stats(dist_matrix,clustering = cl$clustering)
#     return(c(k,cs$ch,cs$avg.silwidth))
# }


# find_optimal_clusters <- function(seq_dist, k_range=c(2:10)){
#     cl_stats <- data.frame(matrix(NA,nrow=length(k_range),ncol=3))
#     for (i in k_range){
#         cl_stats[i,] <- get_pam_cluster_stats(seq_dist,i)    
#     }
#     return (cl_stats)
# }


evaluate_cluster_stats <- function(seq_dist,seq_wts,k_range){
    clus_stats <- wcKMedRange(seq_dist, weights=seq_wts, kvals=k_range)
    return(clus_stats)
}

pam_clustering <- function(seq_dist,seq_wts,k,cluster_method,seed=1729){
    # Clustering of the distance matrix using PAM/k-medoids alogirthm

    # Parameters:
    #   seq_dist: the distance matrix
    #   k: number of clusters
    # Returns:
        # cluster_pam: PAM cluster object which contains medoid IDs, cluster labels, etc.
    set.seed(seed)
    if (cluster_method=="PAM"){
        cluster_pam <- pam(seq_dist, k=k, diss = TRUE)
    }else{
        cluster_pam <- wcKMedoids(seq_dist,weights=seq_wts,k=k,cluster.only=TRUE,npass=5)
    }
    
    return (cluster_pam)
}


save_cluster_results <- function(seq_obj,seq_dist,clusters,clus_res_path,cluster_method){
    cus_nr <-  rownames(seq_obj)

    # Based on datastructure of output when using PAM function
    if(cluster_method=="PAM"){
        cluster_labels <- clusters$clustering
        medoids <- rep(0,dim(seq_obj)[1])
        dist_to_med <- rep(0,dim(seq_obj)[1])
        medoids[clusters$id.med] <- 1
        df_cluster_results <-  data.frame(customer_nr=cus_nr, cluster=cluster_labels, medoids=medoids,dist_to_med=dist_to_med)

        for (i in c(1:length(clusters$id.med))){
            df_cluster_results$dist_to_med[df_cluster_results$cluster == i] <- as.matrix(seq_dist)[df_cluster_results$cluster == i,clusters$id.med[i]]
        }
    }else{    
    # Based on datastructure of output when using wcKMedoids function
        medoid_ids <- unique(clusters$clustering)
        cluster_labels <- match(clusters$clustering,medoid_ids)
        medoids <- as.integer(c(1:dim(seq_obj)[1]) %in% medoid_ids)
        dist_to_med <- rep(0,dim(seq_obj)[1])
        df_cluster_results <-  data.frame(customer_nr=cus_nr, cluster=cluster_labels, medoids=medoids,dist_to_med=dist_to_med)

        for (i in c(1:length(medoid_ids))){
            df_cluster_results$dist_to_med[df_cluster_results$cluster == i] <- as.matrix(seq_dist)[df_cluster_results$cluster == i,medoid_ids[i]]
        }
    }
    
    df_cluster_results <- df_cluster_results[order(df_cluster_results$cluster, df_cluster_results$dist_to_med),]
    df_cluster_results <- df_cluster_results[,1:3]
    write.csv(df_cluster_results,row.names=FALSE,file=paste0(clus_res_path,".csv"))
}

trim_seq <- function(array){
  new_arr <- array[1]
  for (i in c(2:length(array))){
    if(array[i] != array[i-1]){
      new_arr <- c(new_arr,array[i])
    }
  }
  arr_str <- paste0(new_arr,collapse = ", ")
  return(arr_str)
}

get_seq_file_name <- function(params){
    seq_name <- paste0('sequence_',params$country,'_',params$season,'_',params$min_trip,'d_to_',
        params$max_trip,'d_WDaligned_',params$align_by_day_of_week,'_win_',params$window_hrs,'_wCtry',params$country_for_missing)
    
    return (seq_name)
}



