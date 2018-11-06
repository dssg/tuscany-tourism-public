import os
import sys
import unidecode
from colorsys import hls_to_rgb
from colormap import rgb2hex

from shapely.geometry.polygon import Polygon
from shapely.geometry.multipolygon import MultiPolygon
import pandas as pd
import numpy as np

from bokeh.io import show, output_file
from bokeh.models import ColumnDataSource, HoverTool, PanTool, WheelZoomTool, LinearColorMapper, CategoricalColorMapper, BasicTicker, ColorBar
from bokeh.palettes import brewer
from bokeh.plotting import figure, save
from bokeh.transform import transform

def plot_location_cluster(df_clusters,
                          to_drop = 5,
                          path_to_file='',
                          file_name=''):
    """
    Create a fancy html visualization with bokeh.

    Paramaters:
        df_clusters: GeoDataFrame containing the shape files, municipality codes and cluster labels
        to_drop: minimum number of municipalities in a cluster to color. If a cluster contains fewer municipalities, their appear white.
        path_to_file: str, path to the results folder
        file_name: str, results name file
    """

    # expand multipolygons into multiple lines
    shp_expanded = df_clusters.set_index(['PRO_COM'])['geometry'].apply(pd.Series).stack().reset_index()
    shp_expanded.rename(columns = {0: 'geometry'}, inplace = True)
    df_exp = shp_expanded.merge(df_clusters.drop(columns = 'geometry'), on = 'PRO_COM', how = 'left')

    # drop municipalities (i.e., make them white in the plot)
    df_exp['labels_count'] = df_exp.groupby('labels')['labels'].transform('count')
    df_exp.loc[df_exp['labels_count'] < to_drop, 'labels'] = 100000

    # renumber the clusters
    values = np.arange(1, df_exp['labels'].unique().size+1)
    keys = sorted(df_exp['labels'].unique())
    df_exp['labels'] = df_exp['labels'].map(dict(zip(keys, values)))

    # Get lat lon from geometry to plot
    df_toplot = df_exp.drop('geometry', axis=1).copy()
    df_toplot['x'] = df_exp.apply(getGeometryCoords,
                                  geom='geometry',
                                  coord_type='x',
                                  shape_type='polygon',
                                  axis=1)
    df_toplot['y'] = df_exp.apply(getGeometryCoords,
                                  geom='geometry',
                                  coord_type='y',
                                  shape_type='polygon',
                                  axis=1)

    # create colormap
    cs = create_funky_cmap(len(list(map(str, sorted(df_toplot['labels'].unique()))))-1)
    colors = []
    for c in cs:
        r, g, b = c
        colors.append(rgb2hex(r, g, b))
    colors.append("#ffffff") # make last cluster white

    # remove non unicode characters
    df_toplot['COMUNE'] = df_toplot['COMUNE'].apply(unidecode.unidecode)

    # Make LocationClusterMap
    mapper = CategoricalColorMapper(palette=colors,factors=list(map(str, sorted(df_toplot['labels'].unique()))))
    source = ColumnDataSource(data=dict(
                              x=df_toplot['x'],
                              y=df_toplot['y'],
                              name=df_toplot['COMUNE'],
                              similar=df_toplot['similar'],
                              label=df_toplot['labels'].astype(str)))
    p = figure(
        x_axis_location=None, y_axis_location=None,
        plot_width=800, plot_height=700)

    p.grid.grid_line_color = None
    p.outline_line_color = None
    p.title.align = "center"
    p.title.text_font_size="40px"

    p.patches('x', 'y', source=source,
              fill_color=transform('label', mapper),
              fill_alpha=0.8, line_color="lightgray", line_width=0.3)

# color_bar = ColorBar(color_mapper=mapper, ticker=BasicTicker(),
#                  label_standoff=12, border_line_color=None, location=(0,0))
# p.add_layout(color_bar, 'right')

    #Add tools
    hover= HoverTool(tooltips = [
        ("Comune","@name"),
        ("Most similar (ordered)","@similar"),
        ("Cluster number:", "@label")
        ])
    p.add_tools(PanTool(), WheelZoomTool(), hover)

    if not os.path.exists(path_to_file):
        os.makedirs(path_to_file)
    output_file(path_to_file+file_name)
    save(p)


def create_funky_cmap(n_colors):
    """
    Create a color map for coloring clusters

    Paramters:
        n_colors: number of colors in the colormap

    Returns:
        colors: list of colors
    """

    colors = []
    for i in np.arange(0., 360., 360. / n_colors):
        h = i / 360.
        l = (50 + np.random.rand() * 10) / 100.
        s = (90 + np.random.rand() * 10) / 100.
        colors.append(tuple((256*np.array(list(hls_to_rgb(h, l, s)))).astype(int)))

    return colors

# get external coordinates from polygons
# from Sam, @ DSSG chicago
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
