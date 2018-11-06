"""
This script contains the preprocessing functions for the Geo2vec input. The
input consists of a list of strs, each of them containing a location code.
"""

import numpy as np

def str_to_list(df_trips):
    """
    Convert a str (output of the SQL query) into a list of strs

    Parameters:
	df_trips: DataFrame containing the column 'locations'
    """

    # replace str of geolocations by a list of strs with geolocation codes
    df_trips['locations_list'] = df_trips['locations'].str.split(', ').tolist()

    # drop old column to save memory
    df_trips.drop('locations', axis=1, inplace=True)

    # find length of the individual trips
    df_trips['trip_len'] = df_trips['locations_list'].apply(len)

    print('\nNumber of individual trips:', df_trips.shape[0])


def filter_short_trips(df_trips, min_length=1):
    """
    Remove short trips from the trips DataFrame

    Parameters:
	df_trips: DataFrame containing the complete trip list and the 'trip_len' column
	min_length: minimum length of the trips to keep

    Return:
	df_trips_red: the reduced DatFrame containing trips bigger than min_length
    """

    # remove trips shorter than min_length
    df_trips_red = df_trips[df_trips['trip_len'] > min_length]

    print('\nReduced number of individual trips:', df_trips_red.shape[0])

    return df_trips_red


def descriptive_sanity_check(df_trips):
    """
    Run a simple descriptive sanity check on the trips DataFrame, by printing useful parameters

    Parameters:
	df_trips: DataFrame with the trips and a 'trip_len' column
    """

    print('\nMean number of visited municipalities =',
    np.round(df_trips['trip_len'].mean(), 2))
    print('Median number of visited municipalities =', int(df_trips['trip_len'].median()))
    print('Min number of visited municipalities =', df_trips['trip_len'].min())
    print('Max number of visited municipalities =', df_trips['trip_len'].max())
