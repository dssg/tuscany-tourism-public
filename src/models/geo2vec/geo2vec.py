import os
import time
import pickle

import numpy as np
import pandas as pd
from sklearn import cluster
from sklearn.manifold import TSNE
from sklearn.metrics import silhouette_score, calinski_harabaz_score
import gensim

import matplotlib
matplotlib.use('Agg')
import matplotlib.pylab as plt


class Geo2vec:
    """
    The geo2vec model. Based on word2vec, this model train embedding vectors
    for geolocations (i.e. cities, provinces, etc) and cluster them using
    k-means. The clusters contain locations that typically appear in a given
    sequences based on the 'context' (nearby locations in the sequences).
    """

    def __init__(self, emb_size, window_size, season, country):
        """
        Parameters:
            emb_size: Number of dimensions for the embedding vectors
            window_size: Maximum range of municipalities to be taken into
                         account while training the model
        """

        self.emb_size = emb_size
        self.window_size = window_size
        self.season = season
        self.country = country

        self.model_name = 'emb'+str(self.emb_size)+\
                          '_wind'+str(self.window_size)+\
                          '_epochs0'

        self.model_dir = 'trained_models/'+self.country+'_'+self.season+'/'
        self.model_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), self.model_dir)
        self.model_file = os.path.join(self.model_path, self.model_name)

        self.df_dir = 'clusters_geodataframes/'+self.country+'_'+self.season+'/'
        self.df_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), self.df_dir)
        self.df_file = os.path.join(self.df_path, self.model_name)

        # create necessary folders
        if not os.path.exists(self.model_path):
            os.makedirs(self.model_path)
        if not os.path.exists(self.df_path):
            os.makedirs(self.df_path)


    def initialize(self, sequences=None, min_count=1):
        """
        Initialize geo2vec model

        Parameters:
            sequences: DataFrame containing all the trips as sequences of strs,
                       where each string is a geolocation
        """

        # check is model has already been initialized
        if os.path.exists(self.model_file):
            self.g2v = gensim.models.Word2Vec.load(self.model_file)
            print('\nGeo2vec model has already been initialized. Loading previously initialized model...')

        # if no model is initialized, need to give a sequence!
        elif sequences is None:
            print('\nGeo2vec model has not been initialized. Please provide an input sequence of locations.')
            return

        # initialize new model
        else:

            print('\nInitializing Geo2vec model... (this might take a few minutes)')
            tic = time.time()
            self.g2v = gensim.models.Word2Vec(sequences,
                                              size=self.emb_size,
                                              window=self.window_size,
                                              sg=1,
                                              hs=0,
                                              min_count=min_count,
                                              workers=20)
            toc = time.time()
            self.save()
            print('Geo2vec model initialized in', int(toc-tic), 'seconds.')

        self.n_epochs_trained = 0

        # create embeddings
        self.vocab = list(self.g2v.wv.vocab)
        self.embeddings = self.g2v[self.vocab]


    def train(self, sequences, n_epochs=1):
        """
        Train the geo2vec model with given hyperparameters.
        By default, save all models in the subfolder 'g2v_models'

        Parameters:
            sequences: DataFrame containing all the trips as sequences of strs,
                       where each string is a geolocation
            n_epochs: Number of epochs to train the model
        """

        # check if model was already trained
        self.n_epochs_trained += n_epochs


        # check is model has already been initialized
        self.model_name = 'emb'+str(self.emb_size)+\
                          '_wind'+str(self.window_size)+\
                          '_epochs'+str(self.n_epochs_trained)
        self.model_file = os.path.join(self.model_path, self.model_name)
        if os.path.exists(self.model_file):
            self.g2v = gensim.models.Word2Vec.load(self.model_file)
            print('\nGeo2vec model has already been trained. Loading previously trained model...')

        else:
            # train model
            print('\nTraining model for', n_epochs, 'epochs...')

            tic = time.time()
            self.g2v.train(sequences,
                           total_examples=sequences.shape[0],
                           epochs=n_epochs)

            # update embeddings
            self.vocab = list(self.g2v.wv.vocab)
            self.embeddings = self.g2v[self.vocab]
            self.save()
            toc = time.time()
            print('Geo2vec model trained in', int(toc-tic), 'seconds.')

            self.df_file = os.path.join(self.df_path, self.model_name)


    def create_clusters(self, n_clusters):
        """
        Create cluster labels using k-means.
        Append the cluster label and embedding vectors to a pandas DataFrame

        Parameters:
            n_clusters: Number of clusters to use for k-means
        """

        self.n_clusters = n_clusters
        kmeans = cluster.KMeans(n_clusters=self.n_clusters,
                                random_state=42)
        kmeans.fit(self.embeddings)
        labels = kmeans.labels_

        #'loc_code', 'embeddings', and'labels' are the geolocations,
        # the embedding vectors and the cluster labels, respectively
        self.df_labels = pd.DataFrame({'loc_code': list(map(int, self.vocab)),
                                       'embeddings': self.embeddings.tolist(),
                                       'labels': labels})


    def merge_gdf(self, gdf_to_merge, column='PRO_COM'):
        """
        Merge cluster label to a given GeoDataFrame. The labels are stored in
        self.df_labels['loc_code'].

        Parameters:
            gdf_to_merge: GeoDataFrame to merge the cluster labels
            column: str, name of the column containing the area codes
        """

        self.gdf_clusters = gdf_to_merge.merge(self.df_labels,
                                               how='inner',
                                               left_on=column,
                                               right_on='loc_code')

    def get_most_similar(self, n_similar=3):
        """
        Get most similar locations using the embedding vector.

        Parameters:
            n_similar: number of similar municipalities to find
        """

        def get_similar(pro_com, topn=n_similar):

            list_of_similars = self.g2v.wv.most_similar(str(pro_com), topn=topn)

            l = []
            for s in list(map(int, [c[0] for c in list_of_similars])):
                l.extend(self.gdf_clusters.loc[self.gdf_clusters['PRO_COM'] == s, 'COMUNE'])
            return l

        self.gdf_clusters['similar'] = self.gdf_clusters['PRO_COM'].apply(get_similar)


    def apply_tsne_2D(self):
        """
        Apply t-sne to visualize the clusters in 2D
        see: https://stackoverflow.com/questions/43776572/visualise-word2vec-generated-from-gensim

        Parameters:
            gdf_mun: GedoDataFrame with location codes
        """

        print('\nCalculating t-SNE... (this may take a few minutes)')

        tsne = TSNE(n_components=2)
        df_tsne = pd.DataFrame(tsne.fit_transform(self.embeddings),
                               index=self.vocab,
                               columns=['x', 'y'])

        # add COR_PRO and COD_REG to df_tsne for a colorful plot
        df_tsne['loc_code'] = df_tsne.index.astype(int)
        self.df_tsne = pd.merge(df_tsne,
                                self.df_labels,
                                left_on='loc_code',
                                right_on='loc_code',
                                how='inner')


    def plot_tsne_2D(self, path_to_save='', save=True):
        """
        Plot the 2D t-SNE map
        """

        fig = plt.figure(figsize=(13, 13))
        ax = fig.add_subplot(1, 1, 1)

        ax.scatter(self.df_tsne['x'], self.df_tsne['y'],
                   c=self.df_tsne['labels'],
                   cmap='jet')

        plt.axis('off')
        if save:
            plt.savefig(path_to_save+'t-sne.png')


    def save(self):
        """
        Save an initialized or trained model.
        """
        self.g2v.save(self.model_file)
        print('\nGeo2vec model', self.model_name, 'saved at', self.model_path)


    def load(self, n_epochs_trained):
        """
        Load a pre-trained model.

        Parameters:
            model_name: the str with the name of the model to be loaded
            n_epochs_trained: number of trained epochs of the model to load
        """

        # check if model already exists
        self.n_epochs_trained = n_epochs_trained
        self.model_name = 'emb'+str(self.emb_size)+\
                          '_wind'+str(self.window_size)+\
                          '_epochs'+str(self.n_epochs_trained)
        self.model_file = os.path.join(self.model_path, self.model_name)
        if os.path.exists(self.model_file):
            self.g2v = gensim.models.Word2Vec.load(self.model_file)

            # create new embeddings
            self.vocab = list(self.g2v.wv.vocab)
            self.embeddings = self.g2v[self.vocab]

            print('Model',self.model_name,'successfully loaded.')

        # if not, complain
        else:
            print('Model has not been trained for',n_epochs_trained,'epochs.',
                  'Please run model.train(n_epochs) to create the model.')


    def pickle_cluster_labels(self, tag=''):
        """
        Save the dataframe containing

        Paramters:
            tag: str, tag to add to the  file name
        """

        pickle_path = self.df_file+'_clus'+str(self.n_clusters)+'_'+tag
        self.gdf_clusters.to_pickle(pickle_path, compression='gzip')


    def print_params(self):
        """
        Print current model parameters.
        """

        print('\n\nGeo2vec model details:\n')
        print('Model name:', self.model_name)
        #print('Model path:', self.model_path)
        print('Season:', self.season)
        print('Country:', self.country)
        print('Window Size =', self.window_size)
        print('Embedding dimension =', self.emb_size)
        print('Trained epochs =', self.n_epochs_trained)
