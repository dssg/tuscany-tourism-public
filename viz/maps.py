import os
import sys

import numpy as np
import pandas as pd
import geopandas as gpd

import matplotlib
import matplotlib.cm as cm
import matplotlib.pylab as plt
from matplotlib.colors import Normalize
import matplotlib.animation as animation
from cycler import cycler
from colorsys import hls_to_rgb
from shapely.geometry import Point

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
        colors.append(hls_to_rgb(h, l, s))

    return colors



class Map:
    """
    A map as a geopandas object containing shape files
    """

    def __init__(self, gdf_map):
        """
        Initialize a Heatmap objects

        Parameters:
            gdf_map: GeoDataFrame to be plotted
            """

        self.fig = plt.figure(figsize=(13,13))
        self.ax = self.fig.add_subplot(1,1,1)
        self.fontsize = 20

        self.city_markersize = 6
        self.city_marker = 'o'
        self.city_markercolor = 'k'

        self.map = gdf_map


    def plot(self):
        """
        Plot a simple map
        """

        self.map.plot(ax=self.ax,
                      color='white',
                      edgecolor='gray')

        plt.axis('off')


    def important_cities(self,
                         cities_path=r"/mnt/data/shared/important_cities.csv"):
        """
        Include important cities in the plot. The csv city file must have the 'lat', 'long' and 'city' columns.

        Parameters:
            cities_path: str containing the math to a csv file with the 'lat',
                         'long' and 'city' name of the cities to include in the
                         plot
        """

        df_cities = pd.read_csv(cities_path)

        for i, name in enumerate(list(df_cities.city)):
            plt.plot(df_cities.long[i], df_cities.lat[i],
                     marker=self.city_marker,
                     color=self.city_markercolor,
                     markersize=self.city_markersize)

            plt.annotate(name,
                         (df_cities.long[i]+0.03, df_cities.lat[i]),
                         fontsize=self.fontsize)


    def save(self, path):
        """
        Save heatmap

        Parameters:
            path: str, the path to save the heatmap
        """

        plt.savefig(path, transparent=True)



class Heatmap(Map):
    """
    The heatmap based on a geopandas objects containing shape files
    """

    def __init__(self, gdf_map):
        """
        Initialize a Heatmap objects

        Parameters:

            gdf_map: GeoDataFrame to be plotted
        """

        self.fig = plt.figure(figsize=(13,13))
        self.ax = self.fig.add_subplot(1,1,1)
        self.fontsize = 18

        self.city_markersize = 6
        self.city_marker = 'o'
        self.city_markercolor = 'k'
        self.cmap = 'Reds'

        self.map = gdf_map


    def replace_zeros(self):
        """
        Replace zeros from the column to plot
        """

        min_c = np.array(self.map[self.column])
        self.map.loc[self.map[self.column]==0, self.column] = np.min(min_c[np.nonzero(min_c)])


    def plot(self, column=False):
        """
        Plot the heatmap for the column 'column'. If column == False, plot a
        simple map

        Paramters:
            column: str, the name of the column used for the heatmap
        """

        if not column:

            self.map.plot(ax=self.ax,
                          color='white',
                          edgecolor='gray')

        else:

            self.column = column

            # remove zeros to avoid erros when plotting
            # there are 6 municipalities in Tuscany with 0 towers or visits:
            # Capolona, Molazzana, Sassetta, Casale Maritimo, Filattiera, Tresana
            self.replace_zeros()

            self.min = self.map[column].min()
            self.max = self.map[column].max()
            self.range = np.linspace(self.map[column].min(),
                                     self.map[column].max(),
                                     num=5)

            self.map.plot(column=self.column,
                          ax=self.ax,
                          cmap=self.cmap,
                          alpha=0.7,
                          edgecolor='gray')
        plt.axis('off')


    def plot_log(self, column, log_min=False, log_max=False):
        """
        Plot the log heatmap for the column 'column'

        Parameters:
            column: str, the column to be used for the heatmap
            log_min: minimun value for the log plot. If False, the minimum of
                     'column' is used
            log_max: maximun value for the log plot. If False, the maximun of
                     'column' is used
        """

        self.column = column

        # create the new log column
        self.column_log = column+'_log'
        self.map[self.column_log] = np.log(self.map[self.column])

        # cash some useful values for the plot
        if (log_min is False) or (log_max is False):
            self.min = np.round(self.map[self.column_log].min(), 6)
            self.max = np.round(self.map[self.column_log].max(), 6)
        else:
            self.min = np.round(log_min, 6)
            self.max = np.round(log_max, 6)

        self.range = np.linspace(self.min, self.max, num=5)

        # remove zeros to avoid erros when plotting
        # there are 6 municipalities in Tuscany with 0 towers or visits:
        # Capolona, Molazzana, Sassetta, Casale Maritimo, Filattiera, Tresana
        self.replace_zeros()

        self.map.plot(column=self.column_log,
                      ax=self.ax,
                      vmin=self.min,
                      vmax=self.max,
                      cmap=self.cmap,
                      alpha=0.7,
                      edgecolor='gray')
        plt.axis('off')


    def colorbar(self):
        """
        Add a colorbar to the heatmap
        """

        norm = Normalize(vmin=self.min, vmax=self.max)
        n_cmap = cm.ScalarMappable(norm=norm, cmap='Reds')
        n_cmap.set_array([])

        cbar = self.ax.get_figure().colorbar(n_cmap,
                                             fraction=0.03,
                                             ticks=self.range)
        cbar.ax.set_yticks(self.range)

        if hasattr(self, 'column_log'):
            cbar.ax.set_yticklabels((np.exp(self.range)/1000).astype(int),
                                     fontsize=self.fontsize)
        else:
            cbar.ax.set_yticklabels((self.range/1000).astype(int),
                                     fontsize=self.fontsize)
        cbar.ax.set_ylabel('Number of unique visitors (thousands)',
                           rotation=270,
                           labelpad=25,
                           fontsize=self.fontsize+1)



class LocationsClustermap(Map):
    """
    The cluster based on a geopandas objects containing shape files and cluster
    labels
    """

    def plot(self, column, path_to_save='', file_params='', save=True):

        self.column = column
        if not os.path.exists(path_to_save) and save:
            os.makedirs(path_to_save)

        # find number of clusters
        self.n_clusters = self.map[column].nunique()

        # create colormap
        cs = create_funky_cmap(self.n_clusters)
        self.cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", cs)

        print('Number of clusters:', self.n_clusters)

        self.map.plot(column=column,
                      ax=self.ax,
                      cmap=self.cmap,
                      categorical=True,
                      alpha=0.7,
                      edgecolor='white')

        plt.axis('off')
        if save:
            plt.savefig(path_to_save+'Location_cluster'+file_params+'.png')



class TrajectoryClustermap(Map):
    """
    This map plots the scatter plot of the centroids of turists trajectories,
    with different colors for different clusters.
    """

    def __init__(self, gdf_map, path_to_centroids=''):
        """
        Initialize a TrajectoryClustermap objects

        Parameters:
            gdf_map: GeoDataFrame to be plotted (typically the municipalities
                     for all Italy)
            path_to_centroids: str, path to a file containing the controids of
                               each municipality
            """
        
        plt.switch_backend('agg')
        self.fig = plt.figure(figsize=(13,15))
        self.ax = self.fig.add_subplot(1,1,1)
        self.fontsize = 20

        self.city_markersize = 6
        self.city_marker = 'o'
        self.city_markercolor = 'k'

        self.map = gdf_map
        self.df_centroids = pd.read_csv(path_to_centroids)


    def plot_medoids(self, df_clusters, path_to_save='', file_name='', save=True):
        """
        Plot the medoid trajectories in a single map

        Parameters:
            df_clusters: DataFrame with the output of the sequence clustering
                         model. It must cointain the columns 'location_list',
                         'cluster' and 'medoids', containing the list of
                         location trips (list of strs), the cluster labels and
                         the medoid flag (1 for medoid, 0 otherwise)
        """

        # plot background map
        self.plot()

        # create colormap for trajectories
        self.clusters = df_clusters['cluster'].unique()
        self.n_clusters = len(self.clusters)

        # separate medoids
        df_med = df_clusters[df_clusters['medoids'] == 1]

        # cluster loop
        for c in self.clusters:

            df_clus = df_med[df_med['cluster'] == c]

            trip = list(map(int, df_clus['locations_list'].tolist()[0]))
            df_trip = pd.DataFrame(data={'pro_com': trip})

            # get centroids of each trip
            self.df_trip_entroids = self.get_centroids_trip(df_trip)
            self.plot_single_trajectory()
            
        if save:
            plt.savefig(path_to_save+file_name+'_cluster_summary.png')
     

    def plot_samples(self, df_clusters, n_trajectories_per_cluster=5, path_to_save='', file_name='', save=True):
        """
        Plot a sample of the trajectories from each cluster

        Parameters:
            df_clusters: DataFrame with the output of the sequence clustering
                         model. It must cointain the columns 'location_list',
                         'cluster' and 'medoids', containing the list of
                         location trips (list of strs), the cluster labels and
                         the medoid flag (1 for medoid, 0 otherwise)

            n_trajectories_per_cluster: number of trajectories to plot per
                                        cluster
        """


        # create colormap for trajectories
        self.clusters = df_clusters['cluster'].unique()

        # cluster loop
        for c in self.clusters:

            self.fig = plt.figure(figsize=(13,15))
            self.ax = self.fig.add_subplot(1,1,1)

            # plot background map
            self.plot()

            df_clus = df_clusters[df_clusters['cluster'] == c]
            # Separate medoids. Always plot medoids. Medoids are cool.
            df_med_clus = df_clus[df_clus['medoids'] == 1]

            trip = list(map(int, df_med_clus['locations_list'].tolist()[0]))
            df_trip = pd.DataFrame(data={'pro_com': trip})
            # get centroids of each trip
            self.df_trip_entroids = self.get_centroids_trip(df_trip)
            self.plot_single_trajectory()


            # trajectory loop
            if n_trajectories_per_cluster > 1:

                df_sample = df_clus[df_clus['medoids'] == 0][:n_trajectories_per_cluster-1]

                for t in range(n_trajectories_per_cluster-1):

                    trip = list(map(int, df_sample.iloc[[t], :]['locations_list'].tolist()[0]))
                    df_trip = pd.DataFrame(data={'pro_com': trip})
                    # get centroids of each trip
                    self.df_trip_entroids = self.get_centroids_trip(df_trip)
                    self.plot_single_trajectory()
            
            if save:
                cluster_wise_plot_path = path_to_save+"clusterwise_trajectories/"
                if not os.path.exists(cluster_wise_plot_path):
                    os.makedirs(cluster_wise_plot_path)
                plt.savefig(cluster_wise_plot_path+file_name+'_clusterwise_trajectories_'+str(c)+'.png')

    def plot_trajectories_heatmap(self, df_clusters, gdf_map, path_to_save='', file_name='', save=True):

        """
        Plot the trajectories in a cluster in the form of a heatmap

        Paramters:
            df_clusters: DataFrame with the output of the sequence clustering
                         model. It must cointain the columns 'location_list',
                         'cluster' and 'medoids', containing the list of
                         location trips (list of strs), the cluster labels and
                         the medoid flag (1 for medoid, 0 otherwise)
            gdf_map: GeoDataFrame to be plotted (typically the municipalities
                     in Tuscany)
        """

        # List of clusters for plots
        self.clusters = df_clusters['cluster'].unique()

        # cluster loop
        for c in self.clusters:

            self.fig = plt.figure(figsize=(12,10))
            self.ax = self.fig.add_subplot(1,1,1)

            self.map_forheat = gdf_map

            # plot background map
            self.map_forheat.plot(ax=self.ax,
                                  color='white',
                                  edgecolor='gray')

            df_clus = df_clusters[df_clusters['cluster'] == c]

            # create list of municipalities for all the trips in a single cluster
            trips = []
            for t in range(df_clus.shape[0]):
                trips.extend(list(map(int, df_clus.iloc[[t], :]['locations_list'].tolist()[0])))

            df_trips = pd.DataFrame(data={'pro_com': trips})
            df_counts = df_trips['pro_com'].value_counts().rename_axis('pro_com').reset_index(name='counts')

            # counts for each municipality
            self.map_forheat = self.map_forheat.merge(df_counts,
                                                      how='left',
                                                      left_on='PRO_COM',
                                                      right_on='pro_com').fillna(0)

            # min and max for colorbar
            self.min = self.map_forheat['counts'].min()
            self.max = self.map_forheat['counts'].max()
            self.range = np.linspace(self.map_forheat['counts'].min(),
                                     self.map_forheat['counts'].max(),
                                     num=5)

            self.map_forheat.plot(column='counts',
                                  ax=self.ax,
                                  cmap='Reds',
                                  alpha=0.7,
                                  edgecolor='gray')

            # include colorbar
            norm = Normalize(vmin=self.min, vmax=self.max)
            n_cmap = cm.ScalarMappable(norm=norm, cmap='Reds')
            n_cmap.set_array([])
            cbar = self.ax.get_figure().colorbar(n_cmap,
                                                 fraction=0.03,
                                                 ticks=self.range)
            cbar.ax.set_yticks(self.range)
            cbar.ax.set_yticklabels((self.range).astype(int),
                                             fontsize=self.fontsize)
            cbar.ax.set_ylabel('Number of unique visitors of cluster '+str(c),
                                   rotation=270,
                                   labelpad=25,
                                   fontsize=self.fontsize+1)

            self.important_cities()

            plt.axis('off')
            if save:
                heatmaps_plot_path = path_to_save+"clusterwise_heatmaps/"
                if not os.path.exists(heatmaps_plot_path):
                    os.makedirs(heatmaps_plot_path)
                plt.savefig(heatmaps_plot_path+file_name+'_heatmap_cluster'+str(c)+'.png')


    def get_centroids_trip(self, trip):
        """
        Merge controids of municipalities to DataFrame

        Parameters:
            trip: DataFrame with municipalities in a trip (column format)
        """

        self.trip_centroids = trip.merge(self.df_centroids,
                                    how='inner',
                                    left_on='pro_com',
                                    right_on='pro_com')


    def plot_single_trajectory(self):
        """
        Plot a single trajectory
        """

        plt.plot(self.trip_centroids['lon'], self.trip_centroids['lat'], '-o')



class Featuresmap(Map):
    """
    The map plots the feature clusters.
    """


    def plot_clusters(self, df_labeled, df_reg_tus):
        """
        Plot top cluters by size on the map of Tuscany at the territory level

        Parameters:
            df_labeld: Dataframe of unscaled feature with cluster labels
            df_reg_tusc: shape file of Tuscany
        """

        self.plot()
        
        cluster_names=df_labeled['label'].value_counts().index

        for c in cluster_names:
            cluster = df_labeled[df_labeled['label']==c]

            # filter only tuscany
            geometry = [Point(xy) for xy in zip(cluster['avg_lon'], cluster['avg_lat'])]
            cluster = cluster.drop(['avg_lon', 'avg_lat'], axis=1)
            geo_cluster = gpd.GeoDataFrame(cluster, crs=df_reg_tus.crs, geometry=geometry)
            tusc_mask = geo_cluster.within(df_reg_tus.loc[8, 'geometry'])
            self.cluster_tusc = geo_cluster.loc[tusc_mask]

            self.cluster_tusc.plot(ax=self.ax, markersize=1.2, alpha=0.4, label='Cluster '+str(c))

        leg = plt.legend(loc='best', fontsize=self.fontsize, markerscale=20)
