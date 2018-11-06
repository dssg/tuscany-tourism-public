# This is file contains a python script to combine the municipalities (comunes) in Tuscany into the 28 districts
# (territories) predefined by the local authorities, and export a shapefile of Tuscany with the 28 territories

# Importing libraries

import sys
sys.path.append("..")
import geopandas as gpd
import pandas as pd

# load shapefile at the comune level 
municipalities = r"/mnt/data/shared/Boundaries regions and municipalities Italy 2016/Com2016_WGS84_g/Com2016_WGS84_g.shp"


# Select only Tuscany 
df_mun = gpd.read_file(municipalities)
df_mun_tusc = df_mun[df_mun["COD_REG"] == 9]

# Convert coordinates in WGS84 to Lat Lon format (DO NOT use for the _github files)
# see http://geopandas.org/projections.html
df_tusc['geometry'] = df_tusc['geometry'].to_crs(epsg=4326)
df_mun_tusc['geometry'] = df_mun_tusc['geometry'].to_crs(epsg=4326)


## List of territories and corresponding comunes
dist_comu = pd.read_csv('/mnt/data/ywang99587/TPT/comuni2district.csv')
dist_comu.Comuni=dist_comu.Comuni.str.title()
df_mun_tusc.COMUNE = df_mun_tusc.COMUNE.str.title()

## Make sure numbers are the same - two 'extra' comunes because Tuscany did not decide to which territory they belong, use the territory map as reference
df_mun_tusc_sub = df_mun_tusc[df_mun_tusc['COMUNE'].isin(dist_comu.Comuni)]
dist_comu_sub = dist_comu[dist_comu['Comuni'].isin(df_mun_tusc.COMUNE)]

## Join and merge comunes to territories
df_mun_tusc_sub_dis = df_mun_tusc_sub.set_index('COMUNE').join(dist_comu.set_index('Comuni'), how='left')
df_dist = df_mun_tusc_sub_dis.dissolve(by='District')

df_dist['District'] = df_dist.index
df_dist['rown']=list(range(1,len(df_dist)+1))

df_mun_tusc_sub_dis.merge(df_dist[['District', 'rown']], on='District' )[['PRO_COM','rown']].to_csv('/mnt/data/shared/com_conv_to_district.csv', index=False)


## Write to shapefile
df_dist.to_file('/mnt/data/shared/ITA_shapefiles/Tus_28districts.shp')
