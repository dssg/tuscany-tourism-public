import os
import sys
r_path_data = "../src/models/kmeans/"
sys.path.append(r_path_data)
from kmeans import *
from create_interactive_chart import *


r_path_data = "../src/utils/load_data/"
sys.path.append(r_path_data)
from load_dataframes import *

import geopandas as gpd
from shapely.geometry import Point


# Airport arrivals

airport_cities_d = {"airport": ['Pisa', 'Florence'], 
         "lat": [43.7228, 43.7696], "lon": [10.4017, 11.2558]}

def create_airports(data):
    """
    Create airport geodataframe based on lat and lon of cities
    Exmaple: 
    data = airport_cities_d = {"airport": ['Pisa', 'Florence'], 
         "lat": [43.7228, 43.7696], "lon": [10.4017, 11.2558]}
    """
    
    airport_cities = pd.DataFrame(data)
    geometry = [Point(xy) for xy in zip(airport_cities.lon, airport_cities.lat)]
    airport_cities = airport_cities.drop(['lon', 'lat'], axis=1)
    crs = {'init': 'epsg:4326'}
    geo_airport_cities = gpd.GeoDataFrame(airport_cities, crs=crs, geometry=geometry)
    return geo_airport_cities


def get_airport_start_end(result, geo_airport_cities):
    """
    Add Pisa and FLorence airport data to result dataframe
    Function checks whether the first arrival to Italy is within the area of Pisa and Florence airport.
        Input: result, geo_airport_cities geodataframe
        Output: 'geometry_st': boolean, arrived by plane
                'geometry_end' : boolean, left by plane
                'geometry_st_fl': boolean, arrived to Florence airport
                'geometry_end_fl': boolean, left from Florence airport
                'geometry_st_pisa': boolean, arrived to Pisa airport
                'geometry_end_pisa': boolean, left from Pisa airport
                
    """
    crs={'init': 'epsg:4326'}
    geometry_st = [Point(xy) for xy in zip(result.start_lon, result.start_lat)]
    geometry_end = [Point(xy) for xy in zip(result.end_lon, result.end_lat)]
    geo_st = gpd.GeoDataFrame(geometry_st, crs=crs, geometry=geometry_st)[['geometry']]
    geo_end = gpd.GeoDataFrame(geometry_end, crs=crs, geometry=geometry_end)[['geometry']]
    geo_st.crs = crs
    geo_end.crs = crs
    st_airport = pd.DataFrame(geo_st.within(geo_airport_cities['geometry'].unary_union.buffer(0.1)))
    st_airport.index=result.index
    result['geometry_st'] = st_airport
    end_airport = pd.DataFrame(geo_end.within(geo_airport_cities['geometry'].unary_union.buffer(0.1)))
    end_airport.index=result.index
    result['geometry_end'] = end_airport
    st_florence = pd.DataFrame(geo_st.within(geo_airport_cities['geometry'].loc[1].buffer(0.1)))
    st_florence.index=result.index
    result['geometry_st_fl'] = st_florence
    end_florence = pd.DataFrame(geo_end.within(geo_airport_cities['geometry'].loc[1].buffer(0.1)))
    end_florence.index=result.index
    result['geometry_end_fl'] = end_florence
    st_pisa = pd.DataFrame(geo_st.within(geo_airport_cities['geometry'].loc[0].buffer(0.1)))
    st_pisa.index=result.index
    result['geometry_st_pisa'] = st_pisa
    end_pisa = pd.DataFrame(geo_end.within(geo_airport_cities['geometry'].loc[0].buffer(0.1)))
    end_pisa.index=result.index
    result['geometry_end_pisa'] = end_pisa
    return result


def add_airport_arrivals(result, airport_cities_d):
    """"
   Add airport arrival data to clsutering result data
        result: clustering result with customer features
   New columns: 'geometry_st': boolean, arrived by plane
                'geometry_end' : boolean, left by plane
                'geometry_st_fl': boolean, arrived to Florence airport
                'geometry_end_fl': boolean, left from Florence airport
                'geometry_st_pisa': boolean, arrived to Pisa airport
                'geometry_end_pisa': boolean, left from Pisa airport
    """
    geo_airport_cities=create_airports(airport_cities_d)
    result=get_airport_start_end(result, geo_airport_cities)
    return result


#Create descriptive helper functions


def cluster_airport_result(result, i, var):
    """
    Calculate how many % of a cluster arrived/left by plane, from Florence and Pisa airport.
    Return a string as a description.
    result: clustering result with customer features
    var: 'label': k-means results
         'cluster': trajectory results
    i: cluster label
    """
    
    cus=result[result[var]==i]
    arrive_by_plane=np.round(cus['geometry_st'].sum()/len(cus)*100,2)
    left_by_plane=np.round(cus['geometry_end'].sum()/len(cus)*100,2)
    arrive_fl=np.round(cus['geometry_st_fl'].sum()/len(cus)*100,2)
    arrive_pis= np.round(cus['geometry_st_pisa'].sum()/len(cus)*100,2)
    st_end_fl=pd.crosstab(cus['geometry_st_fl'],cus['geometry_end_fl']).apply(lambda x: x / x.sum()*100, 1).round(2)[True][True]
    st_end_pis=pd.crosstab(cus['geometry_st_pisa'],cus['geometry_end_pisa']).apply(lambda x: x / x.sum()*100, 1).round(2)[True][True]
    res=f'{arrive_by_plane}% arrived to, and {left_by_plane}% left by plane from Tuscany. '
    res=res+f'{arrive_fl}%  arrived to Florence airport and {arrive_pis}% landed in Pisa. '
    res=res+f'{st_end_fl}% of those who arrived to Florence by plane left from the same airport. '
    res=res+f'{st_end_pis}% of those who arrived to Pisa airport left by plane from Pisa too. '
    return res


def calculate_cluster_size(result, var):
    """
    Calculate clluster sizes, absed on result dataframe
    result: clustering result with customer features
    var: 'label': k-means results
         'cluster': trajectory results
    returns a dataframe with cluster size and ratio
    """
    
    cluster_results=pd.DataFrame(result[var].value_counts())
    ratio=np.round(cluster_results/cluster_results.sum()*100, 2).rename(columns={var:"ratio"})
    return cluster_results.join(ratio)

def cluster_size(result, var):
    """
    Helper function for cluster size only (not rounded)
    """
    df=calculate_cluster_size(result, var)
    df['cus']=df.index
    return df


def create_basic_description(result, season, country, var):
    """
    Returns the season, number of tourists by country, and the successrate of clustering
    input:
    result: clustering result with customer features
    var: 'label': k-means results
         'cluster': trajectory results
    season: names of the season used for clustering
    country: name of the country (all=all country)
 
    """
    if country!='all':
        return f'In the {season} season {(len(result))} tourists visited Tuscany from {country.title()}, we managed to cluster {np.round(len(result[pd.notnull(result[var])])/len(result)*100,2)}% of them.'
    else:
        return f'In the {season} season {(len(result))} tourists visited Tuscany, we managed to cluster {np.round(len(result[pd.notnull(result[var])])/len(result)*100,2)}% of them.'

    
def get_top_nationalities(result, n=5):
    """
    Returns top n nationalities  within the sample
    n: number of top countries to print out
    result: clustering result with customer features
    """
    nat_freq=pd.DataFrame(result['country'].value_counts())
    ratios=nat_freq[:n]/nat_freq.sum()*100
    res='The most common visitors are from'
    for i in range(0,len(ratios)):
        if i!=len(ratios)-1:
            res=res+f' {ratios.index[i]} ({np.round(ratios.country[i],2)}%),'
        else:
            res=res+f' and {ratios.index[i]} ({np.round(ratios.country[i],2)}%).'
    return res


def get_cluster_baiscs(result, cluster_names, var):
    """
    Returns cluster basic statistics: number of clusters, and their size
    var: 'label': k-means results
         'cluster': trajectory results
    """
    clusters=calculate_cluster_size(result, var)
    res=f'We have {len(clusters)} clusters,'
    for i in zip(range(0,len(clusters)), cluster_names[:len(clusters)]):
        if i[0]!=len(clusters)-1:
            #print(i)
            res=res+f' the {i[1]} cluster represents {clusters.ratio.iloc[i[0]]}%,'
        else:
            res=res+f' and the {i[1]} cluster is {clusters.ratio.iloc[i[0]]}%.'
    return res

def get_cluster_country_distr(result, var):
    """
    Helper function to return cluster's country distribution
    result: clustering result with customer features
    var: 'label': k-means results
         'cluster': trajectory results
    """
    return pd.crosstab(result.country, result[var]).apply(lambda x: x / x.sum()*100, 0).round(2)

def hours_tusc(result, var):
    """
    Helper funcion, which calculates how many hours customers spend in Tuscany
    result: clustering result with customer features
    var: 'label': k-means results
         'cluster': trajectory results
    """
    return np.round(pd.DataFrame(result.groupby(var)[['hrs_in_tusc']].mean())/24)


def get_hours_by_cities(result, var):
    """
    Helper function returns how many hours on avergae each cluster spent in cities in Tuscany
    result: clustering result with customer features
    var: 'label': k-means results
         'cluster': trajectory results
    """
    return pd.DataFrame(result.groupby(var)[['arezzo', 'florence', 'grosseto', 'livorno',
       'lucca', 'pisa', 'pistoia', 'siena', 'coast']].mean()/60).T



def get_places_at_least4_hours(result, cluster, var):
    """
    Returns cities where the given cluster sent at least 4 hours (half a day)
    result: clustering result with customer features
    var: 'label': k-means results
         'cluster': trajectory results
    cluster: cluster label (int)
    """
    
    hours=get_hours_by_cities(result, var)
    four_hours_top=hours.sort_values(cluster, ascending=False)
    cities=four_hours_top[four_hours_top[cluster]>4].index
    if len(cities)==0:
        res='but on average none of the main cities more than 4 hours. '
    else:
        res='out of which at least a half day in'
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


def cluster_mcc_ratio(result, cluster_names, var, n=5):
    """
    Returns top country distribution (n) by clusters, average time spent in Tuscany, 
    places visited (at least 4 hours) and airport sumamry statistics (arrived/left to Pisa, FLorence)
    result: clustering result with customer features
       var: 'label': k-means results
            'cluster': trajectory results
         n: number of top countries to print out  
        nc: number of clusters
    """
    rel1=get_cluster_country_distr(result, var)
    clusters=calculate_cluster_size(result, var)
    hours=hours_tusc(result, var)
    res=""
    for i in zip(clusters.index, cluster_names[:len(clusters)]):
        res=res+f"By the number of unique visitors the {i[1]} cluster's top 5 countries are; "
        rel=rel1.sort_values(i[0],ascending=False)[:n]
        for j in range(0,5):
            if j!=n-1:
                res=res+f'{rel[i[0]].index[j]} ({rel[i[0]][j]}%), '
            else:
                res=res+f'and {rel[i[0]].index[j]} ({rel[i[0]][j]}%). '
                res=res+f'This cluster spends on average {int(hours.hrs_in_tusc[i[0]])} days in Tuscany, '
                res=res+get_places_at_least4_hours(result, i[0], var)
                res=res+ cluster_airport_result(result, i[0], var)
    return res


# Trajectpry Clustering
def join_customer_features(traj_result, username, season, country):
    """
    Returns a dataframe with trajectory clustering results and customer features joined
    Params:
    traj_result: dataframe with trajectory clustering result: customer_nr,column called cluster
    username: username to access aws
    season: season for clustering used 
    country: country used for clustering (note: there is NO option for all)
    """
    user_features=get_k_means_data(username,season, country).set_index("customer_nr")
    features_with_trajectory=user_features.join(traj_result.set_index('customer_nr')[["cluster"]])
    return features_with_trajectory


def trajectory_cluster_description(result, cluster_names, var):
    """
    Returns a description about each cluster:
        how much time they spent in Tuscany
        places visited (at least 4 hours spent)
        airport arrivals and departures
    """
    hours=hours_tusc(result, var)
    nc=len(hours)
    res=''
    if var=='label':
        st=0
    else:
        st=1
    for i in zip(range(st,nc), cluster_names[:nc]):
        res=res + f'The {i[1]} cluster '
        res=res + f'spends on average {int(hours.hrs_in_tusc[(i[0])])} days in Tuscany, '
        res=res+get_places_at_least4_hours(result, i[0], var)
        res=res+ cluster_airport_result(result, i[0], var)
    return res


def write_file(country, season, final, var):
    """
    write out the print into a file at the result folder
    """
    if var=='label':
        path='../results/kmeans/'
    elif var=='cluster':
        path='../results/sequence_analysis/'
    country_ = country.lower()
    season_ = season.replace('-','_')
    file_name=country_+"_"+season_
    newpath=path+file_name+'/'
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    f = open(newpath+file_name+".txt","w")   
    f.write(final)
    f.close()


def get_trajectory_description(traj_result, username, season, country, var, cluster_names,print_it=True):
    """
    Prints out description for clusters
    Params:
    traj_result: dataframe with trajectory clustering result: customer_nr,column called cluster
    username: username to access aws
    season: names of the season used for clustering
    country: name of the country (all=all country)
    var: 'label': k-means results
         'cluster': trajectory results
    """
    result=join_customer_features(traj_result, username, season, country)
    result=add_airport_arrivals(result, airport_cities_d)
    final=(create_basic_description(result, season, country, var)
    +" "+trajectory_cluster_description(result, cluster_names, var))
    if print_it==True:
         write_file(country, season, final, var)
    print(final)


def get_kmeans_description(result, season, country, var, nc, n, cluster_names, print_it=True):
"""
    Prints out description for clusters
    Params:
    result: clustering result with customer features
    season: names of the season used for clustering
    country: name of the country (all=all country)
    var: 'label': k-means results
         'cluster': trajectory results
    n: number of nationalities listed in description, if country=='all'
    names: cluster names
"""
    
    cluster_names=calculate_cluster_size(result, 'label').index
    result=add_airport_arrivals(result,airport_cities_d)
    if country=='all':
        final=(create_basic_description(result, season, country, var)
        +' '+get_top_nationalities(result, n=5)
        +' '+get_cluster_baiscs(result, cluster_names, var)
        + ' \n'+cluster_mcc_ratio(result, cluster_names, var))
    else:
        final=(create_basic_description(result, season, country, var)+' '+
        trajectory_cluster_description(result, cluster_names, var))
    if print_it==True:
         write_file(country, season, final, var)
    print(final)

