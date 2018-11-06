import os.path
import json
import pickle
import sys

import pandas as pd
import geopandas as gpd
import numpy as np

from shapely.geometry.polygon import Polygon
from shapely.geometry.multipolygon import MultiPolygon

from bokeh.io import show, output_file
from bokeh.models import ColumnDataSource, HoverTool, PanTool, WheelZoomTool, CategoricalColorMapper, BasicTicker, ColorBar
from bokeh.palettes import brewer 
from bokeh.plotting import figure, save
from bokeh.transform import transform

sys.path.append("../src/utils/")
from load_data import load_dataframes as load_df
sys.path.append("../src/utils/geolocation/")
import preprocessing
from read_shapefiles import read_files
from geo2vec import Geo2vec
sys.path.append("../viz")
from fancy_maps import plot_location_cluster as plt_loc

def run(params):
    """
    Runs the Geo2vec model based on the params input
    """
    
    username = params['username']
    season = params['season']
    country = params['country']
    EMB_SIZE = params['EMB_SIZE']
    WINDOW_SIZE = params['WINDOW_SIZE']
    N_EPOCHS = params['N_EPOCHS']
    N_CLUSTERS = params['N_CLUSTERS']
    MIN_LENGTH = params['MIN_LENGTH']
    MIN_COUNT = params['MIN_COUNT']
    train_model = params['train_model']
    apply_tsne = params['apply_tsne']
    plot_clusters_italy=params['plot_clusters_italy']
    plot_clusters_tuscany=params['plot_clusters_tuscany']
    path_to_shapefiles = "../src/utils/read_shapefiles/"
    path_to_final_plots = "../results/geo2vec/"
                         
                         
    #####################################
    # Preprocessing                     #
    #####################################
    # load locations data
    if country == 'all':
        df_trips = load_df.get_geo2vec_data_all_country(username, season).rename(columns={'com_locs_trunc':'locations'})
    else:
        df_trips = load_df.get_geo2vec_data(username, season, country).rename(columns={'com_locs_trunc':'locations'})
        
    preprocessing.str_to_list(df_trips)
    df_trips_red = preprocessing.filter_short_trips(df_trips, min_length=MIN_LENGTH)
    preprocessing.descriptive_sanity_check(df_trips_red)

    ####################################
    # Load data from shapefiles        #
    ####################################
    path_shapefiles, regions, provinces, territories, municipalities, crs = read_files.read_shapefile_data(path_to_shapefiles, 'shape_files_path.json')
    df_mun = read_files.read_shapefiles_in(False, path_shapefiles, municipalities, crs)
    df_mun_tus = read_files.read_shapefiles_in(True, path_shapefiles, municipalities, crs)
    #df_ter_tus = read_files.read_shapefiles_in(True, path_shapefiles, territories, crs, apply_crs=False)

    ###################################
    # Geo2vec model                   #
    ###################################
    g2v = Geo2vec(EMB_SIZE, WINDOW_SIZE, season, country)
    # initialize model
    g2v.initialize(sequences=df_trips_red['locations_list'], min_count=MIN_COUNT)
    # train model
    if train_model:       
        g2v.train(df_trips_red['locations_list'], n_epochs=N_EPOCHS)
    g2v.print_params()
    # cluster model
    g2v.create_clusters(n_clusters=N_CLUSTERS)
    

    # save clusters for Italy
    # careful here: plotting Italy generates a HUGE html file
    if plot_clusters_italy:
        print('\nITALY -- plotting...')
        g2v.merge_gdf(df_mun)
        g2v.get_most_similar()
        g2v.pickle_cluster_labels(tag='Italy')       
        plt_loc(g2v.gdf_clusters,
                path_to_file=path_to_final_plots+'{}_{}/'.format(country, season),
                file_name='Location_cluster_Italy_EMB{}_WIN{}_EPO{}_CLU{}_MinL{}_MinC{}.html'.format(EMB_SIZE, WINDOW_SIZE, N_EPOCHS, N_CLUSTERS, MIN_LENGTH, MIN_COUNT))
        
        
    # save clusters for Tuscany
    if plot_clusters_tuscany:
        print('\nTUSCANY -- plotting...\n\n')
        g2v.merge_gdf(df_mun_tus)
        g2v.get_most_similar()
        g2v.pickle_cluster_labels(tag='Tuscany')   
        plt_loc(g2v.gdf_clusters,
                path_to_file=path_to_final_plots+'{}_{}/'.format(country, season),
                file_name='Location_cluster_Tuscany_EMB{}_WIN{}_EPO{}_CLU{}_MinL{}_MinC{}.html'.format(EMB_SIZE, WINDOW_SIZE, N_EPOCHS, N_CLUSTERS, MIN_LENGTH, MIN_COUNT))
    
    # Apply t-SNE to visualize the clusters
    if apply_tsne:
        g2v.apply_tsne_2D()
        g2v.plot_tsne_2D(path_to_save=path_to_final_plots+'{}_{}/'.format(country, season))
