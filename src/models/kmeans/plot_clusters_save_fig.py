import sys
import os
sys.path.append("../src/utils/")
from read_shapefiles import read_files

import sys
r_path_data1 = "../viz/"
sys.path.append(r_path_data1)
from maps import Featuresmap

def read_tusc(path):
    """Helper function to read in the Tuscany shapefile"""
    path_shapefiles, regions, provinces, territories, municipalities, crs = read_files.read_shapefile_data(path, 'shape_files_path.json')
    df_reg_tus = read_files.read_shapefiles_in(True, path_shapefiles, regions, crs)
    
    return df_reg_tus


df_reg_tus=read_tusc("../src/utils/read_shapefiles/")


def plot_clusters(country, result, season, df_reg_tus):
    """
    Visualiza and save the cluster result on the map of Tuscany
    """
    path='../results/kmeans/'
    file_name=country+"_"+season
    newpath=path+file_name+'/'
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    fm=Featuresmap(df_reg_tus)
    fm.plot_clusters(result, df_reg_tus)
    fm.save(newpath+file_name)