# coding: utf-8

# Create location table to add to database
# Created by: Orsi Vasarhelyi
# Contact: orsolya.vasarhelyi@gmail.com
# Last updated: 23.07.2017.


# Generates final location feature table:
# for each coordinate it checks wether a 
# location is in any of the vornois of a tower and adds:
# natural resources (based on shapefiles)
# attractions (based on points of interest)
# coast
# major cities



# connect db
import sys
sys.path.append("..")


#from .application.app.folder.file import func_name

#read shapefiles
r_path = "../new_codebase/src/utils/read_shapefiles/"
json_file = 'shape_files_path.json'
sys.path.append(r_path)
from read_files import read_shapefile_data, read_shapefiles_in


## vornois
import pandas as pd
import geopandas as gpd
import numpy as np
from shapely.geometry import Point
import shapely



path = '../new_codebase/src/utils/read_shapefiles/'
json_file = 'shape_files_path.json'




path = '../new_codebase/src/utils/read_shapefiles/'
json_file = 'shape_files_path.json'
path_out='../shared/'
outfile='location_features.csv'


# get shapefiles

path_shapefiles,regions,provinces,_,municipalities,crs=read_shapefile_data(path,json_file)
df_mun_tusc = read_shapefiles_in(True, path_shapefiles, municipalities, crs)


# get vornois
path='/mnt/data/shared/Voronois/'
vor_s = gpd.read_file(path+'locations_with_voronois_shapes.shp')


# Natural resources

def places_in_tusc(row):
    if row['osm_id'] in places_in_tusc_list:
        return 1
    else:
        return 0

path_to_nat = '../shared/ITA_location_features/italy-natural-shape/natural.shp'


def natural_resources_read(path_to_nat, crs):    
    natural_resources = gpd.read_file(path_to_nat)
    natural_resources['geometry'] = natural_resources['geometry'].to_crs(epsg=4326)
    natural_resources.crs = crs
    return natural_resources


def create_places_in_tusc_list(natural_resources,df_mun_tusc):
    places_in_tusc_list=list(gpd.sjoin(natural_resources, df_mun_tusc, op='intersects')['osm_id'])
    return places_in_tusc_list


natural_resources=natural_resources_read(path_to_nat, crs)
places_in_tusc_list=create_places_in_tusc_list(natural_resources,df_mun_tusc )


def create_natural_resources(natural_resources,places_in_tusc_list, df_mun_tusc, path_to_nat): 
    natural_resources['tusc'] = natural_resources.apply(places_in_tusc,1)
    natural_resources_tuscany = natural_resources[natural_resources['tusc']==1]
    natural_resources_tuscany = natural_resources_tuscany.drop(columns=['tusc'])
    return natural_resources_tuscany


natural_resources_tuscany=create_natural_resources(natural_resources,places_in_tusc_list, df_mun_tusc, path_to_nat)


def join_vors_with_nat_resouces(natural_resources_tuscany, vor_s):
    G = natural_resources_tuscany["geometry"].apply(lambda geom: geom.wkb)
    natural_resources_tuscany = natural_resources.loc[G.drop_duplicates().index]
    vor_with_nat_res = gpd.overlay(vor_s, natural_resources_tuscany, how='intersection')
    return vor_with_nat_res

def calculate_area(vor_with_nat_res):
    for i in vor_with_nat_res['type'].value_counts().index:
        vor_with_nat_res[i+'_area'] = vor_with_nat_res[vor_with_nat_res['type']==i].area.astype(float)
    vors_with_nat_res_area = vor_with_nat_res[['location_i',"forest_area","water_area","park_area","riverbank_area"]].groupby('location_i').sum()
    return vors_with_nat_res_area

vor_with_nat_res=join_vors_with_nat_resouces(natural_resources_tuscany, vor_s)
vors_with_nat_res_area=calculate_area(vor_with_nat_res)

# Add points of interests

points_file="points_of_interest.csv"
def points_of_interests_to_geo(path,points_file):
    points_of_interests = pd.read_csv(path+points_file).set_index('Unnamed: 0')
    points_of_interests = points_of_interests.dropna(subset=['lng', 'lat'])
    points_of_interests['geometry'] = points_of_interests.apply(lambda x: Point((float(x.lng), float(x.lat))), axis=1)
    geo_points_of_interests = gpd.GeoDataFrame(points_of_interests)
    geo_points_of_interests.crs =  crs
    return geo_points_of_interests

geo_points_of_interests=points_of_interests_to_geo(path,points_file)


def join_num_attractions(vor_s,geo_points_of_interests, vors_with_nat_res_area):
    vor_park_points=gpd.sjoin(vor_s, geo_points_of_interests[['type', 'geometry']], op='contains')
    vor_park_points_attrs=vor_park_points[vor_park_points['type']=='attrazioni']
    vor_park_points_attrs['num_attractions']=1
    vor_park_points_attr_sum=vor_park_points_attrs[['location_i','num_attractions']].groupby('location_i').sum()
    vors_with_parks_attractions=vors_with_nat_res_area.join(vor_park_points_attr_sum.rename(columns={'type':'num_attractions'}))
    return vors_with_parks_attractions.replace(np.nan,0)

vors_with_parks_attractions=join_num_attractions(vor_s,geo_points_of_interests, vors_with_nat_res_area)

# Add coast

def cal_coast(path_shapefiles, municipalities, crs, df_mun_tusc):
    df_it = read_shapefiles_in(False, path_shapefiles, municipalities, crs).unary_union.boundary
    tusc=df_mun_tusc.unary_union.boundary
    coast=tusc.intersection(df_it)
    return coast

def get_coast(row):
    if type(row[0])==shapely.geometry.multilinestring.MultiLineString or "LINESTRING" in str(row[0]):
        return 1
    else:
        return 0

coast=cal_coast(path_shapefiles, municipalities, crs, df_mun_tusc)


def add_coast(vor_s,vors_with_parks_attractions,coast):
    vors_with_parks_att=vor_s.set_index("location_i").join(vors_with_parks_attractions)
    coast_points=vors_with_parks_att.intersection(coast)
    cp=pd.DataFrame(coast_points)
    cp['coast']=cp.apply(get_coast,1)
    del cp[0]
    vors_with_parks_attrs_coast=vors_with_parks_att.join(cp)
    return vors_with_parks_attrs_coast


vors_with_parks_attrs_coast=add_coast(vor_s,vors_with_parks_attractions,coast)

# Add cities

cities=['Arezzo', 
        'Carrara', 
        'Firenze', 
        'Grosseto', 
        'Livorno', 
        'Lucca', 
        'Pisa',
        'Pistoia',
        'Siena']

def add_cities(vors_with_parks_attrs_coast, cities,df_mun_tusc):
    for city in cities:
        if city in df_mun_tusc['COMUNE'].value_counts().index:
            c=df_mun_tusc[df_mun_tusc['COMUNE']==city]
            m=gpd.sjoin(vors_with_parks_attrs_coast, c,  op='intersects')
            m=m.replace(city,1)
            m['location_id']=m.index
            m[city.lower()]=m.groupby('location_id')['COMUNE'].sum()
            vors_with_parks_attrs_coast=vors_with_parks_attrs_coast.join(m[[city.lower()]])
    return vors_with_parks_attrs_coast


vors_with_parks_attrs_coast_cities=add_cities(vors_with_parks_attrs_coast, cities,df_mun_tusc)

# write final data out
vors_with_parks_attrs_coast_cities.to_file(path_out+outfile)

