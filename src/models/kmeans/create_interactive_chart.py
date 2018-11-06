import sys
import os
sys.path.append("../../src/utils/")
from read_shapefiles import read_files

import pandas as pd
import plotly as py
import plotly.graph_objs as go
from shapely.geometry import Point
import geopandas as gpd



def read_tusc(path):
    """
    Helper function to read in the Tuscany shapefile
    """
    path_shapefiles, regions, provinces, territories, municipalities, crs = read_files.read_shapefile_data(path, 'shape_files_path.json')
    df_reg_tus = read_files.read_shapefiles_in(True, path_shapefiles, regions, crs)
    return df_reg_tus


def filter_tusc(result):
    """
    Filter geopoints to get only Tuscany
    """
    geometry = [Point(xy) for xy in zip(result['avg_lon'], result['avg_lat'])]
    df_reg_tus=read_tusc("../src/utils/read_shapefiles/")
    geo_cluster = gpd.GeoDataFrame(result, crs=df_reg_tus.crs, geometry=geometry)
    tusc_mask = geo_cluster.within(df_reg_tus.loc[8, 'geometry'])
    result_tusc = geo_cluster.loc[tusc_mask]
    return result_tusc

def create_file_name_and_path(country, season):
    path='../results/kmeans/'
    country_ = country.lower()
    season_ = season.replace('-','_')
    file_name=country_+"_"+season_
    newpath=path+file_name+'/'
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    return (newpath,file_name)

def create_data(result, names, colors):
    """
    Create data for visulaization
    """
    
    data=[]
    df=filter_tusc(result)
    clusters=df['label'].value_counts().index
    seq = pd.Series([0,1,2,3], index=clusters)
    for i in clusters:
        loc = seq.index.get_loc(int(i))
        x=df[df['label']==i][['avg_lat', 'avg_lon', 'label']]
        site_lat = x.avg_lat
        site_lon = x.avg_lon
        locations_name = x.index
        data.append(go.Scattermapbox(
            lat=site_lat,
            lon=site_lon,
            mode='markers',
            marker=dict(
                size=3,
                color=colors[loc],
                opacity=0.8
            ),
            text=locations_name,
            hoverinfo='none',
            name= names[loc])
        )
    return data

def plot_kmeans(result ,names, colors, country, season, mapbox_access_token):
    """
    Creates and interactive html output of the clusters, if the number of points is more 100K randomly sample 50K of them
    result: Dataframe, constaining  k-means clustering results under the column 'label'
    names: List of cluster names in order
    country: Country to be chosen to perform analyses, if country='all', runs on the full data
    season: Season to be chosen to perform analyses - 'pre-summer', 'summer', 'post-summer', 'winter', or 'all' for the whole year
    mapbox_access_token: your mapbox access token, create here: https://www.mapbox.com/help/how-access-tokens-work/
    """
    
    if len(result)>100000:
        result=result.sample(50000, replace=False)
    d=create_data(result, names, colors)
    layout = go.Layout(
    title=country.title()+" in the "+season.title(),
    autosize=True,
    hovermode='closest',
    showlegend=True,
    mapbox=dict(
        accesstoken=mapbox_access_token,
        bearing=0,
        center=dict(
            lat=43.45089368,
            lon=11.12636257
        ),
        pitch=0,
        zoom=7,
        style='light'
    ),
)

    fig = dict(data=d, layout=layout)
    newpath,filename=create_file_name_and_path(country, season)
    print(newpath,filename)
    py.offline.plot(fig, filename=newpath+filename+'.html')
    return fig