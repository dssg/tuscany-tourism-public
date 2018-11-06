import os
import sys
import numpy as np
import pandas as pd
import geopandas as gpd
import math
from dateutil.relativedelta import relativedelta as rd

import plotly.graph_objs as go
import plotly as py
from plotly.graph_objs import *
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from shapely.geometry.multipolygon import MultiPolygon

from bokeh.io import show, output_file
from bokeh.models import ColumnDataSource, HoverTool, PanTool, WheelZoomTool, LinearColorMapper, ColorBar
from bokeh.palettes import brewer 
from bokeh.plotting import figure, save
from bokeh.transform import transform

r_path = "../../utils/"
sys.path.append(r_path)

from sequence_analysis import sequence_preprocessing as sf
from geolocation import preprocessing as gp
from read_shapefiles import read_files
from load_data import load_dataframes as ld

MAPBOX_ACCESS_TOKEN = 'pk.eyJ1IjoidmFzYXJoZWx5aW8iLCJhIjoiY2prYjV2djh0M2R3NDNxbWw3dTFqdGZvbyJ9.stZ2MjMsogAYJ9fMb-lrsg'

def add_sequence_to_clusters(path_to_cluster_results,file_name,username, season, country, min_trip, max_trip):
    """
    Function to add sequence of communes to the cluster results

    Parameters: 
        path_to_cluster_results: path to the cluster results
        file_name: name of the cluster results file
        username: username to load the data
        season: season of analysis
        country: country of analysis
        min_trip: minimum trip length to subset
        max_trip: maximum trip length to subset

    Returns:
        save the cluster results file with the list of locations
    """
    ## loading the data
    df_trips = ld.get_sequence_data(username, season, country, min_trip, max_trip)
    df_trips = df_trips.drop(['mcc'],axis=1)
    df_trips['customer_nr'] = list(map(int,df_trips['customer_nr']))
    
    ## loading the cluster results
    cluster_results = pd.read_csv(path_to_cluster_results+file_name+".csv")
    cluster_results = cluster_results.loc[:,['customer_nr','cluster','medoids']]
    
    ## merging cluster results with the sequence data and saving it
    cluster_results = cluster_results.merge(df_trips,how='inner',left_on='customer_nr',right_on='customer_nr')
    cluster_results.to_csv(path_to_cluster_results+file_name+".csv")

def plot_clusters(path_to_cluster_results,file_name,plot_medoid_summary=True,plot_each_cluster=True,n_trajectories_per_cluster=4,plot_heatmap=True,save_outputs=True):
    """
    Function to plot the results of the sequence analysis. These are the old matplotlib plots (deprecated, do not use)

    Parameters: 
        path_to_cluster_results: path to the cluster results
        file_name: name of the cluster results file
        plot_medoid_summary: Boolean flag to plot of the medoids of all clusters
        plot_each_cluster: Boolean flag to plot sample trajectories of each cluster
        n_trajectories_per_cluster: Number of sample trajectories to plot in the clusterwise sample
        plot_heatmap: Boolean flag to plot of the Tuscany heatmap for each cluster
        save_outputs: Boolean flag to save the results

    Returns:
        saves the plots in the results folder
    """
    ## loading the cluster data
    cluster_results = pd.read_csv(path_to_cluster_results+file_name+".csv")
    gp.str_to_list(cluster_results)
    r_path = os.path.dirname(os.path.realpath(__file__))
    ## loading the shape files
    path_shapefiles, regions, provinces, territories, municipalities, crs = read_files.read_shapefile_data(r_path+'/../read_shapefiles/', 'shape_files_path.json')
    df_mun = read_files.read_shapefiles_in(False, path_shapefiles, regions, crs)
    df_mun_tus = read_files.read_shapefiles_in(True, path_shapefiles, municipalities, crs)
    r_path = "../viz/"
    ## Initilizing the plot
    t = TrajectoryClustermap(df_mun,path_to_centroids=r_path+"comune_centroids.csv")

    ## Plotting required ones
    if plot_medoid_summary:
        t.plot_medoids(cluster_results, path_to_save=path_to_cluster_results, file_name=file_name, save=True)
    if plot_each_cluster:
        t.plot_samples(cluster_results,n_trajectories_per_cluster, path_to_save=path_to_cluster_results, file_name=file_name, save=True)
    if plot_heatmap:
        t.plot_trajectories_heatmap(cluster_results,df_mun_tus, path_to_save=path_to_cluster_results, file_name=file_name, save=True)
        
        
def plot_interactive_trajectories(path_to_cluster_results,file_name,cluster_names,country,plot_medoid_summary=True,plot_each_cluster=True,n_trajectories_per_cluster=4,save_outputs=True):
    """
    Function to plot the interactive results of the sequence analysis.

    Parameters: 
        path_to_cluster_results: path to the cluster results
        file_name: name of the cluster results file
        plot_medoid_summary: Boolean flag to plot of the medoids of all clusters
        plot_each_cluster: Boolean flag to plot sample trajectories of each cluster
        n_trajectories_per_cluster: Number of sample trajectories to plot in the clusterwise sample
        plot_heatmap: Boolean flag to plot of the Tuscany heatmap for each cluster
        save_outputs: Boolean flag to save the results

    Returns:
        saves the plots in the results folder
    """
    ## loading the cluster data
    df_clusters = pd.read_csv(path_to_cluster_results+file_name+".csv")
    ## loading the centroid of the communes
    df_centroids = pd.read_csv("../../viz/comune_centroids.csv")
    
    colors = ["rgb(57,106,177)","rgb(218,124,48)","rgb(62,150,81)","rgb(204,37,41)","rgb(83,81,84)",\
              "rgb(107,76,154)","rgb(146,36,40)","rgb(148,139,61)"]

    ## creating the Plotly layout 
    layout = Layout(
        autosize=True,
        hovermode='closest',
        mapbox=dict(
            accesstoken=MAPBOX_ACCESS_TOKEN,
            bearing=0,
            style='light',
            center=dict(
                lat=43.45089368,
                lon=11.12636257
            ),
            pitch=0,
            zoom=6
        ),
    )

    ## creating data dictionary for plotly and creating the figure
    if plot_medoid_summary:
        df_med = df_clusters[df_clusters['medoids'] == 1]
        
        traj_percent = []
        for i in df_clusters['cluster'].unique():
            traj_percent.append(np.round(100*df_clusters[df_clusters['cluster'] == i].shape[0]/df_clusters.shape[0], decimals=1))

        ## calling the function to the get the data in the required format
        data = get_data_for_plotly(df_med,df_centroids,colors,cluster_names, label_percent=traj_percent)   
        fig = dict(data=data, layout=layout)
        if save_outputs:
            py.offline.plot(fig, filename=path_to_cluster_results+file_name+"_medoid_summary"+'.html')
        else:
            return fig

    ## creating data dictionary for plotly and creating the figure
    if plot_each_cluster:
        clusters = df_clusters['cluster'].unique()
        n_clusters = len(clusters)
        for i in clusters:
            df_trips_med = df_clusters[(df_clusters['medoids'] == 1) & (df_clusters['cluster'] == i)]
            df_trips_traj = df_clusters[(df_clusters['medoids'] == 0) & (df_clusters['cluster'] == i)][:n_trajectories_per_cluster-1]
            df_trips = pd.concat([df_trips_med,df_trips_traj])
           
            if country in ['Germany', 'France', 'United States', 'Netherlands', 'China']:
                traj_names = get_tourist_names(country)
                np.random.shuffle(traj_names) # shuffle tourist names
            else:
                traj_names = ["Tourist_{n}".format(n=i+1) for i in range(n_trajectories_per_cluster)]

            ## calling the function to the get the data in the required format
            data = get_data_for_plotly(df_trips,df_centroids,colors,traj_names)
            fig = dict(data=data, layout=layout)
            if save_outputs:
                cluster_wise_plot_path = path_to_cluster_results+"clusterwise_trajectories/"
                if not os.path.exists(cluster_wise_plot_path):
                    os.makedirs(cluster_wise_plot_path)
                py.offline.plot(fig, filename=cluster_wise_plot_path+file_name+'_clusterwise_trajectories_'+str(i)+'.html')
            else:
                return fig

def get_data_for_plotly(df_trips,df_centroids,colors,label_names, label_percent='None'):
    """
    Function to get the data dictionary in the form required for plotting on Plotly

    Parameters: 
        df_trips: A dataframe with the sequences for each trajectory to be plotted
        df_centroids: the data frame containing centroids of the communes
        colors: list of colours for each of the trajectories
        label_names: names for each trajectory used in the label
        label_percent: If included, the percent of each group will be mention. Used for the medoid summary

    Returns:
        data: data dictionary needed for plotting using Plotly
    """
    data = []
    ## Looping through each of the sequences in the data frame
    for c in range(0,len(df_trips)):
        
        trip = list(map(int,df_trips['locations'].iloc[c].split(', ')))
        df_trip = pd.DataFrame(data={'pro_com': trip})
        # get centroids of each trip
        df_trip_centroids = get_centroids_trip(df_trip,df_centroids)

        ## appending list of points in the trajectory to plot
        data.append(go.Scattermapbox(
                lat=[df_trip_centroids['lat'][0]],
                lon=[df_trip_centroids['lon'][0]],
                legendgroup= 'T'+str(c),
                mode='markers',
                marker=dict(
                    size=12,
                    color = colors[c],
                    opacity=0.5
                ),
                showlegend=False
                ))
        steps = []
        for i in range(len(df_trip_centroids)):
            steps.append((df_trip_centroids['lat'][i],df_trip_centroids['lon'][i]))
        
        name_to_plot = label_names[c]
        if label_percent != 'None':
            name_to_plot += " ("+str(label_percent[c])+"%)"
            
        ## appending the lines of the trajectory to plot
        data.append(go.Scattermapbox(
                lat=[item_x[0] for item_x in steps],
                lon=[item_y[1] for item_y in steps],
                legendgroup= 'T'+str(c),
                mode='markers+lines',
                text = [str(df_trip_centroids['comune'][j]) for j in range(len(trip))],
                hoverinfo='text',
                name=name_to_plot,
                marker=dict(
                    size=6,
                    color=colors[c]
            ),
                line=dict(
                    width=3,
        )))

    return data


def get_centroids_trip(df_trip,df_centroids):
    """
    Merge controids of municipalities to DataFrame

    Parameters:
    trip: DataFrame with municipalities in a trip (column format)
    """

    trip_centroids = df_trip.merge(df_centroids,
                                how='inner',
                                left_on='pro_com',
                                right_on='pro_com')
    return trip_centroids


def plot_cluster_heatmaps(path_to_cluster_results,file_name):
    """
    Function to plot the interactive heatmap results of the sequence analysis.

    Parameters: 
        path_to_cluster_results: path to the cluster results
        file_name: name of the cluster results file

    Returns:
        saves the plots in the results folder
    """
    r_path = os.path.dirname(os.path.realpath(__file__))
    path_shapefiles, regions, provinces, territories, municipalities, crs = read_files.read_shapefile_data(r_path+'/../read_shapefiles/', 'shape_files_path.json')
    df_mun = read_files.read_shapefiles_in(False, path_shapefiles, regions, crs)
    df_mun_tus = read_files.read_shapefiles_in(True, path_shapefiles, municipalities, crs)

    # expand multipolygons
    shp_expanded = df_mun_tus.set_index(['PRO_COM'])['geometry'].apply(pd.Series).stack().reset_index()
    shp_expanded.rename(columns = {0: 'geometry'}, inplace = True)
    df_mun_tus_exp = shp_expanded.merge(df_mun_tus.drop(columns = 'geometry'), on = 'PRO_COM', how = 'left')

    df_clusters = pd.read_csv(path_to_cluster_results+file_name+".csv")
    gp.str_to_list(df_clusters)

    # create heatmaps gdfs
    for c in df_clusters['cluster'].unique():

        df_clus = df_clusters[df_clusters['cluster'] == c]

        # create list of municipalities for all the trips in a single cluster
        trips = []
        for t in range(df_clus.shape[0]):
            trips.extend(list(map(int, np.unique(df_clus['locations_list'].iloc[t]))))
            

        df_trips = pd.DataFrame(data={'pro_com': trips})
        df_counts = df_trips['pro_com'].value_counts().rename_axis('pro_com').reset_index(name='counts')

        # counts for each municipality
        heatmap_gdf = df_mun_tus_exp.merge(df_counts,
                                                 how='left',
                                                 left_on='PRO_COM',
                                                 right_on='pro_com').fillna(0)

        # Get lat lon from geometry to plot
        heatmap_toplot = heatmap_gdf.drop('geometry', axis=1).copy()

        heatmap_toplot['x'] = heatmap_gdf.apply(getGeometryCoords, 
                                      geom='geometry', 
                                      coord_type='x', 
                                      shape_type='polygon',
                                      axis=1)
                                         
        heatmap_toplot['y'] = heatmap_gdf.apply(getGeometryCoords, 
                                      geom='geometry', 
                                      coord_type='y', 
                                      shape_type='polygon',
                                      axis=1)
        # Make heatmap

        colors = brewer['Reds'][9][::-1]
        mapper = LinearColorMapper(palette=colors,
                                   high=heatmap_toplot['counts'].max(), 
                                   low=heatmap_toplot['counts'].min())
        source = ColumnDataSource(data=dict(
                                         x=heatmap_toplot['x'], 
                                         y=heatmap_toplot['y'],
            name=heatmap_toplot['COMUNE'], 
            count=heatmap_toplot['counts']
        ))

        p = figure(
            x_axis_location=None, y_axis_location=None,
            plot_width=800, plot_height=700
        )
        p.grid.grid_line_color = None
        p.outline_line_color = None
        p.title.align = "center"
        p.title.text_font_size="40px"

        p.patches('x', 'y', source=source,
                  fill_color=transform('count', mapper),
                  fill_alpha=0.8, line_color="gray", line_width=0.3)

        color_bar = ColorBar(color_mapper=mapper, major_label_text_font_size='10pt',
                         label_standoff=12, border_line_color=None, location=(0,0))
        p.add_layout(color_bar, 'right')

        #Add tools
        hover= HoverTool(tooltips = [
            ("Comune","@name"),
            ("Number of visitors","@count")
        ])

        p.add_tools(PanTool(), WheelZoomTool(), hover)
        output_file(path_to_cluster_results+"/clusterwise_heatmaps/"+file_name+"_heatmap_cluster_"+str(c)+".html")
        save(p)


def getGeometryCoords(row, geom, coord_type, shape_type):
    """
    Returns the coordinates ('x' or 'y') of edges of a Polygon exterior.
    
    :param: (GeoPandas Series) row : The row of each of the GeoPandas DataFrame.
    :param: (str) geom : The column name.
    :param: (str) coord_type : Whether it's 'x' or 'y' coordinate.
    :param: (str) shape_type
    """
    
    # Parse the exterior of the coordinate
    if shape_type == 'polygon':
        exterior = row[geom].exterior
        if coord_type == 'x':
            # Get the x coordinates of the exterior
            return list( exterior.coords.xy[0] )    
        
        elif coord_type == 'y':
            # Get the y coordinates of the exterior
            return list( exterior.coords.xy[1] )


def get_tourist_names(country):
    """
    Get five smartly chosen names, typical for each country.
    
    Parameters:
        country: str, the name of the country 
        
    Returns:
        list containing five names to be used in the labels
    """    
    
    if country == 'Germany':
        return ['Jurgen', 'Johannes', 'Helga', 'Anja', 'Gabriele']

    if country == 'France':
        return ['Jean-Pierre', 'Francois', 'Ophelie', 'Celine', 'Melisande']
    
    if country == 'United States':
        return ['Richard', 'Joe', 'Anne', 'Katy', 'Junior']
  
    if country == 'Netherlands':
        return ['Arjan', 'Paul vdB', 'Emma', 'Sophie', 'Vincent']
    
    if country == 'China':
        return ['Qi Wei', 'Yimeng', 'Yanbing', 'Chen Chen', 'Cha Hu']









