# coding: utf-8

# Read shapefiles as a geopandas dataframe
# Created by: Orsi Vasarhelyi
# Contact: orsolya.vasarhelyi@gmail.com
# Last updated: 20.07.2018.

import pandas as pd
import geopandas as gpd

def read_shapefile_data(path,file_name):
    """
    Reads in a json file containing the path to shapefiles,
    on regional, province and municipality level
    and crs foe encoding
    """

    import json

    d=json.load(open(path+file_name))
    path_shapefiles=d["path_shapefiles"]
    regions=d["regions"]
    provinces=d['provinces']
    municipalities=d['municipalities']
    territories=d['area_territoriali']
    crs=d['crs']
    return path_shapefiles,regions,provinces,territories,municipalities,crs



def read_shapefiles_in(only_tusc, path_to_shapefiles, version, crs, apply_crs=True):
    """
    Reads in sahpefiles as a geopandas dataframe
    only_tusc=True, reads in tuscany aonly
    version: regions, province, municipalities
    """

    df=gpd.read_file(path_to_shapefiles+version)
    if only_tusc==True:
        df=df[df['COD_REG'] == 9]
    if apply_crs:
        # territories are already 4326
        df['geometry'] = df['geometry'].to_crs(epsg=4326)
    return df