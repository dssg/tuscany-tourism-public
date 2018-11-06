# Import load data
import sys
r_path_data = "../src/utils/load_data/"
sys.path.append(r_path_data)
from load_dataframes import *

# K-means
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
#from sklearn import metrics
from sklearn.preprocessing import StandardScaler


#should come from a config later
features={"hrs" : ['hrs_in_tusc', 'hrs_outside_tuscany'],
"numlocs" : ['num_loc_in_tusc','num_unique_loc_in_tusc','num_loc_in_italy','num_unique_loc_in_italy'],
"location" : ['forest', 'water', 'river', 'park', 'arezzo', 'florence', 'livorno', 
              'lucca', 'pisa', 'pistoia', 'siena', 'coast', 'num_attrs'],
"latlon" : ['avg_lat', 'avg_lon', 'top_lat','top_lon','start_lat_tusc',
            'start_lon_tusc', 'start_lat', 'start_lon', 'end_lat', 'end_lon', 'std_lat', 'std_lon']}


def choose_features(features, hrs=True, numlocs=True, location=True, latlon=True):
    """
    Returns a list of feature names chosen from the dictionary "features"
    
    Parameters:
    features: a dictionary with keys equal to the arguments of the function, values list of df variables
    hrs: If True, choose feature group that contains hours spent in Tuscany, hours spent outside Tuscany
    numlocs: If True, choose feature group that contains number of locations and number of unique locations visited in Tuscany and Italy
    location: If True, choose feature group that contains time spent (in mumtiples of ) at the locations with respective features, including landscape, cities visited, and total number of attactions visited.
    latlon: If True, choose feature group that contains latitude and longitude of average location, most visited location, start and end location, and standard deviation of all lat/lon
    """
    final_features=[]
    options = [hrs, numlocs, location, latlon]
    for f in zip(options,features.keys()):
        #print (f)
        if f[0]==True:
            final_features.extend(features[f[1]])
    return final_features


def get_excluded_varaibles(all_features, excluded_features):
    """
    Returns a list of feature names to be excluded from feature scaling

    Parameters:
    all_features: List of features returned from choose_featuers for clustering
    excluded_features: List of features in all_features to be excluded from feature scaling
    """
    s = set(all_features)
    return [x for x in all_features if x not in excluded_features]


def standardize_features(df_feature_all, features, hrs, numlocs, location, latlon):
    """
    Returns a DataFrame of all features to be used for k-means clustering, including scaled and non-scaled (i.e., excluded_features)

    Parameters:
    df_feature_all: A DataFrame of all raw features returned from get_k_means_data (see below)
    features: a dictionary with keys equal to the arguments of the function, values list of df variables
    hrs: If True, choose feature group that contains hours spent in Tuscany, hours spent outside Tuscany
    numlocs: If True, choose feature group that contains number of locations and number of unique locations visited in Tuscany and Italy
    location: If True, choose feature group that contains time spent (in mumtiples of ) at the locations with respective features, including landscape, cities visited, and total number of attactions visited.
    latlon: If True, choose feature group that contains latitude and longitude of average location, most visited location, start and end location, and standard deviation of all lat/lon
    """
    #choose features
    final_features=choose_features(features, hrs=True, numlocs=True, location=True, latlon=True)
    df_rel_features=df_feature_all[final_features]
    features_without_std=[f for f in final_features if f[:3]!='std'] #excluding standard deviation for scaling

    # scale variables
    df_to_scale=df_rel_features[features_without_std] 
    scaler = StandardScaler()
    scaled_feature_all = pd.DataFrame(scaler.fit_transform(df_to_scale), columns = df_to_scale.columns, index=df_to_scale.index)
    
    # add non-scaled variables back
    excluded_vars=get_excluded_varaibles(final_features, features_without_std)
    scaled_feature_all[excluded_vars]=df_rel_features[excluded_vars]    
    df_scaled=scaled_feature_all.query('std_lat > 0 & std_lon > 0') #excluding those who do not move
    """DISCUSS IT"""
    return df_scaled


def kmeans_model(df_kmeans, nc, write=False, path="", outfile=""):
    """
    Returns scaled features DataFrame with labels based on k-means

    Parameters:
    df_kmeans: DataFrame returned from standardize_features
    nc: Number of clusters to be used in k-means
    write: If True, write k-means results (features dataframe with cluster labels) to csv file
    path: path to save csv file
    outfile: filename of csv file

    """
    kmeans = KMeans(n_clusters=nc, n_jobs=-1, random_state=321)
    kmeans.fit(df_kmeans)
    labels = kmeans.labels_
    df_kmeans_labeled = df_kmeans
    df_kmeans_labeled['label'] = labels
    if write==True:
        f_kmeans_labeled[['label']].to_csv(path+outfile)
    return df_kmeans_labeled[['label']]


def calculate_cluster_size(kmeans_res):
    """
    Returns basic cluster information: cluster label, size of cluster and fraction of cluster out of all observations

    Parameters: 
    kmeans_res: DataFrame returned from kmeans_model with scaled features and cluster labels
    """
    cluster_results=pd.DataFrame(kmeans_res['label'].value_counts())
    ratio=np.round(cluster_results/cluster_results.sum()*100, 2).rename(columns={'label':"ratio"})
    return cluster_results.join(ratio) 


def get_cluster_results(username, season, country, features, nc,
                        hrs=True, numlocs=True, location=True, latlon=True,
                        write=False, path="", outfile=""):
    """
    Returns unscaled features with cluster labels based on k-means

    Parameters:
        username: Username to access data via get_k_means_data
        season: Season to be chosen to perform analyses - 'pre-summer', 'summer', 'post-summer', 'winter', or 'all' for the whole year
        country: Country to be chosen to perform analyses, if country='all', runs on the full data
        features: a dictionary with keys equal to the arguments of the function, values list of df variables (defoult)
        hrs: If True, choose feature group that contains hours spent in Tuscany, hours spent outside Tuscany
        numlocs: If True, choose feature group that contains number of locations and number of unique locations visited in Tuscany and Italy
        location: If True, choose feature group that contains time spent (in mumtiples of ) at the locations with respective features, including landscape, cities visited, and total number of attactions visited.
        latlon: If True, choose feature group that contains latitude and longitude of average location, most visited location, start and end location, and standard deviation of all lat/lon
        nc: Number of clusters to be used in k-means
        write: If True, write k-means results (features dataframe with cluster labels) to csv file
        path: path to save csv file
        outfile: filename of csv file

    """
    if country=='all':
        df_feature_all=get_k_means_data_for_all_countries(username, season)
    else:   
        df_feature_all=get_k_means_data(username,season, country)
    df_feature_all=df_feature_all.replace(np.nan,0).set_index('customer_nr')
    df_kmeans=standardize_features(df_feature_all, features, hrs=True, numlocs=True, location=True, latlon=True)
    kmeans_res=kmeans_model(df_kmeans, nc, write=False, path="", outfile="")
    print(calculate_cluster_size(kmeans_res))
    return df_feature_all.join(kmeans_res)













