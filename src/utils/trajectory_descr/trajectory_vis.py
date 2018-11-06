import pandas as pd
import numpy as np
import sys
import os

sys.path.append("../")
from read_shapefiles import read_files

# geolocation preprocessing
from geolocation import preprocessing 

from load_data import load_dataframes

import geopandas as gpd
from shapely.geometry import Point

seasons={'pre-summer':'pre-summer season (May 2017)',
        'summer':'summer season (Jun - Aug 2017)>',
        'post-summer':'post-summer season (Sep - Nov, 2017)',
        'winter':'winter season (Dec 2017 - Feb 2018)'}

# Trajectpry Clustering Descriptions
def join_customer_features(traj_result, username, season, country):
    """
    Returns a dataframe with trajectory clustering results and customer features joined
    Params:
    traj_result: dataframe with trajectory clustering result: customer_nr,column called cluster
    username: username to access aws
    season: season for clustering used 
    country: country used for clustering (note: there is NO option for all)
    """
    user_features=load_dataframes.get_k_means_data(username,season, country).set_index("customer_nr")
    features_with_trajectory=user_features.join(traj_result.set_index('customer_nr')[["cluster"]])
    return features_with_trajectory

def write_file(country, season, final, cluster):
    """
    write out the print into a file at the result folder
    """
    path='../../results/sequence_analysis/'
    country_ = country.title()
    file_name=country_+"_"+season+'_'+cluster
    newpath=path+country_+"_"+season+'/'
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    f = open(newpath+file_name+".txt","w")   
    f.write(final)
    f.close()

    
def calc_num_visitors_in_thousands(result):
    """
    Calcualte the number of visitors in thousands based on original data
    """
    return str(int(np.round(len(result)/10000)))


def calc_num_clusters(d):
    """
    Calcualte the number of clusters based on sampled trajectory results csv
    """
    return str(len(d['cluster'].value_counts()))


def calc_hours_italy(results_with_clusters, cluster):
    """
    Calcualte the average number of days spent in Italy by clusters
    """
    return str(np.round(results_with_clusters[results_with_clusters['cluster']==cluster]['hrs_in_italy'].mean()/24,1))


def calc_hours_tuscany(results_with_clusters, cluster):
    """
    Calcualte the average number of days spent in Tuscany by clusters
    """
    return str(np.round(results_with_clusters[results_with_clusters['cluster']==cluster]['hrs_in_tusc'].mean()/24,1))


def get_hours_by_cities(result):
    """
    Helper function returns how many hours on avergae each cluster spent in cities in Tuscany
    result: clustering result with customer features
    var: 'label': k-means results
         'cluster': trajectory results
    """
    return pd.DataFrame(result.groupby('cluster')[['arezzo', 'florence', 'grosseto', 'livorno',
       'lucca', 'pisa', 'pistoia', 'siena', 'coast']].mean()/60).T



def get_places_at_least4_hours(result, cluster):
    """
    Returns cities where the given cluster sent at least 4 hours (half a day)
    result: clustering result with customer features
    var: 'label': k-means results
         'cluster': trajectory results
    cluster: cluster label (int)
    """
    
    hours=get_hours_by_cities(result)
    four_hours_top=hours.sort_values(cluster, ascending=False)
    cities=four_hours_top[four_hours_top[cluster]>4].index
    if len(cities)==0:
        res='do not spend at least a half day in any major Tuscan city. '
    else:
        res='spend at least a half day in'
        i=0
        for city in cities:
            i+=1
            if city=='coast':
                city='the coast'
            if i!=len(cities) and len(cities)!=1:
                res=res+f' {city.title()},'
            elif i==len(cities) and i!=1:
                res=res+f' and {city.title()}. '
            else:
                res=res+f' {city.title()}. '
    return res

def create_medoid_basic_description(results_with_clusters, names, num_clusters):
    """
    Create the basic summary description of medoids
    Parameters:
        results_with_clusters: dataframe, filtered dataset for the sample which has a cluster label
        names: list, cluster names
        num_clusters: int, number of clusters
    """
    cluster_numbers=['first', 'second', 'third', 'forth', 'fifth', 'sixth', "seventh", 'eighth']
    description=''
    for i in range(1,int(num_clusters)+1):
        cluster_number=cluster_numbers[i-1]
        cluster_name=names[i-1]
        avg_num_days_italy=calc_hours_italy(results_with_clusters, i)
        avg_num_days_tuscany=calc_hours_tuscany(results_with_clusters, i)
        cities_results=get_places_at_least4_hours(results_with_clusters, i)
        cluster_medoid_description=f"The {cluster_number} cluster, which we named {cluster_name}, spends on average {avg_num_days_italy} days in Italy, {avg_num_days_tuscany} of which in Tuscany. When in Tuscany, {cluster_name} {cities_results}"
        description=description+cluster_medoid_description
    return description


def create_medoids_summary(season, country, result, d, names):
    """
    Create cluster based summary of medoids' description
    Parameters:
        season: str, season sued to cluster
        country: str, used to cluster
        result: cluster resutls joint to customer features
        d: trajectory clustering results
        names: list of cluster names
    """
    results_with_clusters=result[pd.notnull(result['cluster'])]
    season_name=seasons[season.lower()]
    num_visitors_thousand=calc_num_visitors_in_thousands(result)
    num_clusters=calc_num_clusters(d)
    summary_text=f"""In the last {season_name} roughly {num_visitors_thousand} thousand tourists visited Tuscany from {country.title()}. The data shows us {num_clusters} clusters. Each line in the graph above represents a cluster's typical path that tourists from {country.title()} followed. These paths are displayed as differently-coloured lines in the map here above. \n"""
    summary_text=summary_text+create_medoid_basic_description(results_with_clusters, names, num_clusters)
    print(summary_text)
    write_file(country, season, summary_text, 'summary')
    return summary_text

def preprocess_data_for_heatmaps(d):
    """
    Creates a dataframe for each cluster with the number of visitors in Tuscan municipalities 
    """
    path_shapefiles, regions, provinces, territories, municipalities, crs = read_files.read_shapefile_data('../../src/utils/read_shapefiles/', 'shape_files_path.json')
    df_mun_tus = read_files.read_shapefiles_in(True, path_shapefiles, municipalities, crs)
    shp_expanded = df_mun_tus.set_index(['PRO_COM'])['geometry'].apply(pd.Series).stack().reset_index()
    shp_expanded.rename(columns = {0: 'geometry'}, inplace = True)
    df_mun_tus_exp = shp_expanded.merge(df_mun_tus.drop(columns = 'geometry'), on = 'PRO_COM', how = 'left')

    preprocessing.str_to_list(d)
    preprocessing.descriptive_sanity_check(d)
    heatmap_list = []
    for c in d['cluster'].unique():
        df_clus = d[d['cluster'] == c]

        # create list of municipalities for all the trips in a single cluster
        trips = []
        for t in range(df_clus.shape[0]):
            trips.extend(list(map(int, np.unique(df_clus['locations_list'].iloc[t]))))


        df_trips = pd.DataFrame(data={'pro_com': trips})
        df_counts = df_trips['pro_com'].value_counts().rename_axis('pro_com').reset_index(name='counts')

        # counts for each municipality
        heatmap_list.append(df_mun_tus_exp.merge(df_counts,
                                                 how='left',
                                                 left_on='PRO_COM',
                                                 right_on='pro_com').fillna(0))
    return heatmap_list


def create_cluster_descriptions(d, names, season, country):
    """
    Create the description of clusters
    Parameters:
        d: df, trajectory clustering results
        season: str, season sued to cluster  
        names: list of cluster names
    
    Returns a description for heatmaps and trajectory examples, 
    conatinning the top 3 most visited municipality for each cluster
    """
    cluster_descriptions=[]
    heatmap_list2=preprocess_data_for_heatmaps(d)
    sample_size=len(d)
    season_name=seasons[season.lower()]
    for c in d['cluster'].unique():
        top_3_muns=heatmap_list2[c-1].sort_values('counts', ascending=False)[['COMUNE', 'counts']][:3]
        cluster_name=names[c-1]
        most_visited_munipality=(top_3_muns['COMUNE'].iloc[0]).encode('utf-8')
        ratio_most_visited_municipality=str(np.round((top_3_muns['counts'].iloc[0])*100/sample_size,0))
        second_most_visited_municipality=(top_3_muns['COMUNE'].iloc[1]).encode('utf-8')
        ratio_second_most_visited_municipality=str(np.round((top_3_muns['counts'].iloc[1])*100/sample_size,0))
        third_most_visited_municipality=(top_3_muns['COMUNE'].iloc[2]).encode('utf-8')
        ratio_third_most_visited_municipality=str(np.round((top_3_muns['counts'].iloc[2])*100/sample_size,0))
        cluster_result=f"""In the heatmap above, we can see the density of the visits of all tourists belonging to the <i>{cluster_name}</i> cluster. The darker the colour, the more {cluster_name} visited that municipality during the {season_name}. As we can see from the  heatmap, the majority of the tourists from  this cluster visited {most_visited_munipality} ({ratio_most_visited_municipality}% of the tourists in this cluster). The next most visited municipalities are {second_most_visited_municipality} ({ratio_second_most_visited_municipality}%), and {third_most_visited_municipality} ({ratio_third_most_visited_municipality}%). Besides the heatmap, in the plot above we can see four examples of trajectories of tourists who belong to the {cluster_name} cluster."""
        write_file(country, season, cluster_result, str(c))
        cluster_descriptions.append(cluster_result)
    return cluster_descriptions

        
def trajectory_description(clus_res_path,clus_res_name, country, season, names, username):
    """
    Generates Summary description for medoids and cluster-based description for trajectory clsutering.
    Parameters:
        d: df, trajectory cluster results, contains 'cluster'
        season: str, names of the season used for clustering
        country: str, name of the country (all=all country)
        names: list of cluster names
        username: Redshift username for connecting db
    Returns:
        saves files out to ../results/sequence_analysis/country+_+season
    """
    d=pd.read_csv(clus_res_path+clus_res_name+".csv")
    result=join_customer_features(d, username, season, country)
    medoid_descr=create_medoids_summary(season, country, result, d, names)
    cluster_descriptions=create_cluster_descriptions(d, names, season, country)
    return (medoid_descr, cluster_descriptions)
    