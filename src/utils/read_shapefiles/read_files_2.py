# coding: utf-8

# Read shapefiles as a geopandas dataframe
# Created by: Qiwei Han
# Last updated: 06.08.2018.

import pandas as pd
import geopandas as gpd

def read_shapefile_data(path,file_name, version):
    """
    Reads in a json file containing the path to shapefiles,
    on regional, province and municipality level
    and crs foe encoding
    """

    import json

    d = json.load(open(path+file_name))
    path_shapefiles = d['path_shapefiles']
    version=d[version]
    
    return path_shapefiles, version


def read_shapefiles_in(path_to_shapefile, file_name, version, only_tusc=True, apply_crs=True):
    """
    Reads in sahpefiles as a geopandas dataframe
    only_tusc=True, reads in tuscany aonly
    version: regions, province, municipalities
    """
    path = path_to_shapefile
    path_to_shapefiles, version = read_shapefile_data(path, file_name, version)
    
    df=gpd.read_file(path_to_shapefiles+version)
    if only_tusc==True:
        df=df[df['COD_REG'] == 9]
    if apply_crs:
        # territories are already 4326
        df['geometry'] = df['geometry'].to_crs(epsg=4326)
    return df
