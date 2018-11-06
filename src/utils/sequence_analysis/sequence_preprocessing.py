"""
This script contains the floowing preprocessing functions for the Sequence clustering input.
-- Reformat output from SQL (str_list_to_int_list and str_to_list)
-- Master function for creating sequences (create_sequences)
-- sub-function to create sequences for an individual (create_sequence_for_individual)
-- Function for customer resampling of a time series (location_with_max_time)
-- Save sequence dataframe (save_seq_dataframe)
"""

# importing math for ceiling function

import math
from multiprocessing import Pool
from itertools import repeat
import numpy as np
import pandas as pd

import os
import sys
import time

r_path = "../"
sys.path.append(r_path)

from load_data import load_dataframes as ld

def preprocess_sequences(username, season, country, min_trip, max_trip,align_by_day_of_week,window_hrs,country_for_missing,seq_path,n_threads=1,return_model=False):
    """
    Master function to load, clean and align sequences based on config Parameters
    Parameters:
        username: username to connect to redshift database
        season: season for analysis
        country: country of origin of the tourists
        min_trip: minimum trip length
        max_trip: maximum trip length
        align_by_day_of_week: if sequences should be aligned by day of week of arrival
        window_hrs: window length for sequence
        country_for_missing: if country of origin to be included in the sequence
        n_threads: number of workers to do the analysis

    """

    model_file = seq_path+".csv"

    if not os.path.exists(model_file):
        df_trips = ld.get_sequence_data(username, season, country, min_trip, max_trip)
        df_trips = str_to_list(df_trips)
        df_sequence = create_sequences(df_trips,align_by_day_of_week,window_hrs,country_for_missing,n_threads)

        df_sequence.to_csv(model_file)

    if return_model:
        return model_file


def str_list_to_int_list(array_like):
    """
    Function to map list of strings to list of integers

    Parameters:
    df_trips: DataFrame containing the column 'locations' and 'times'
    """

    return list(map(int,array_like))


# TODO: Merge with Bruno's functions
def str_to_list(df_trips):
    """
    Convert a str (output of the SQL query) into a list of strs

    Parameters:
    df_trips: DataFrame containing the column 'locations' and 'times'
    """

    # replace str of geolocations by a list of strs with geolocation codes
    df_trips['locations'] = list(map(str_list_to_int_list,df_trips['locations'].str.split(', ').tolist()))

    # replace str of geolocations by a list of strs with geolocation codes
    df_trips['times'] = list(map(str_list_to_int_list,df_trips['times'].str.split(', ').tolist()))
    
    return df_trips

def location_with_max_time(array_like):
    """
    Returns the value in array apprearing most frequently

    Parameters:
    array_like: any array
    """
    return np.bincount(array_like).argmax()

def create_sequences(df_trips,align_by_day_of_week=True,window_hrs=3,country_for_missing=True,n_threads=1):
    """
    Create a dataframe of aligned sequences for sequence clustering analysis

    Parameters:
    df_trips: DataFrame containing the column 'locations', 'times', 'st_time','customer_nr','mcc'
    align_by_day_of_week: If True, the sequences are aligned by the day of week of arrival. Else, the sequences are aligned 
        by their respective first day of arrival.
    window_hrs: window size for sequence creation in hours. A sequence would contain a location for every 'window_hrs' 
        from start to end times
    country_for_missing: If True, the location for entries in the sequence when the individual wasn't in Italy would be
        set to the MCC code of the respective country
    n_threads: Number of threads to use in parallel
    """    
    
    create_sequences.df_trips = df_trips.copy()

    # finding the maximum time spent by an individual to set the length fo sequence
    max_time = max(df_trips['en_time'] - df_trips['st_time'])
    ncols = math.ceil(max_time.total_seconds()/(60*60*window_hrs)) + int(24/window_hrs)

    # If aligning by day of week of arrival, we need additional columns 
    # as someone could arrive on a sunday and stay for max_time
    if align_by_day_of_week == True:
        ncols += 6*math.ceil(24/window_hrs)

    # weeks = 10*np.linspace(1,6,6)
    # days= np.linspace(0,6.5,14)
    # columns = np.add.outer(weeks,days).flatten()
    
    # Initialising the sequence dataframe with NAs
    columns = np.linspace(1,ncols,ncols)
    cus_nr = df_trips['customer_nr']

    # Looping through every customer array to create the aligned sequences data frame
    p = Pool(n_threads)
    l = [i for i in range(0,len(cus_nr))]
    sequences_as_lists = p.starmap(create_sequence_for_individual, zip(l, [align_by_day_of_week]*len(cus_nr), [window_hrs]*len(cus_nr), [country_for_missing]*len(cus_nr), [ncols+1]*len(cus_nr)))

    # Converting list of lists into a dataframe
    col_names = ['customer_nr'] + list(map(str,np.linspace(1,ncols,ncols)))
    df_sequence = pd.DataFrame.from_records(sequences_as_lists,columns=col_names)

    # Setting customer number to be the index
    df_sequence = df_sequence.set_index('customer_nr')
    return df_sequence


def create_sequence_for_individual(i,align_by_day_of_week,window_hrs,country_for_missing,ncols):
    """
    Function to create a sequence for one individual

    Parameters:
    i: row of dataframe to be converted to a sequence
    align_by_day_of_week: If True, the sequences are aligned by the day of week of arrival. Else, the sequences are aligned 
        by their respective first day of arrival.
    window_hrs: window size for sequence creation in hours. A sequence would contain a location for every 'window_hrs' 
        from start to end times
    country_for_missing: If True, the location for entries in the sequence when the individual wasn't in Italy would be
        set to the MCC code of the respective country
    ncols: max length of sequence
    """    
    
    # extracting the row for each customer
    df_row = create_sequences.df_trips[i:i+1]
    # df_row = get_row(i)
    cus = int(df_row['customer_nr'].values[0])
    st_wk = pd.to_datetime(df_row['st_time'].values[0]).weekday()
    st_hr = pd.to_datetime(df_row['st_time'].values[0]).hour
    country = (df_row['mcc'].values[0])

    seq = [np.nan] * ncols
    seq[0] = cus
    # Initialising all values on the sequence to be country of origin if set to True
    if country_for_missing == True:
        seq[1:] = [country]*(ncols-1)
    else:
        seq[1:] = [0]*(ncols-1)

    # Creating the Pandas Series object from the list of 'times'
    # Initialising the time array
    timestamps = [np.datetime64(df_row['st_time'].values[0])]

    # Cummulating times spent at each location to create timestamps
    cum_mins = np.cumsum(np.array(list(map(int,df_row['times'].values[0]))))
    timestamps.extend(np.datetime64(df_row['st_time'].values[0]) + cum_mins.astype('timedelta64[m]'))

    # Getting list of locations
    locs = np.array(df_row['locations'].values[0])
    # Defining the Pandas Series object
    ts = pd.Series(locs,dtype=np.int64,index=timestamps)

    # Resampling sequence for the required window size
    # 1 minute resolution before resampling to window_hrs as we want to find the location spent maximum time at in the window
    ts = ts.resample('1T').bfill()
    # Resampling to window_hrs
    ts2 = ts.resample(str(window_hrs)+'H').apply(location_with_max_time)

    # Identifying the columns to insert into
    if align_by_day_of_week == True:
        col_idx_st = int(24/window_hrs)*st_wk + int(st_hr/window_hrs) +1
    else:
        col_idx_st = int(st_hr/window_hrs) +1

    # Inserting location values into the sequence dataframe
    # df_sequence.loc[[cus],columns[col_idx_st:(col_idx_st + len(ts2))]] = ts2.values
    seq[col_idx_st:(col_idx_st + len(ts2))] = ts2.values

    return seq


# function to save sequence dataframe as csv to load into R for clustering analysis
def save_seq_dataframe(df,file_name):
    """
    Save the dataframe of sequences as a csv to models/data folder to be picked up by relevant code for clustering

    Parameters:
    df: the sequence data frame
    file_name: name of csv
    """    

    rel_path = "../../models/sequence_analysis/data/sequences/"
    df.to_csv(rel_path+file_name)

def create_paths(params):
    """
    Function to create paths to store intermediary objects as well as final results

    Params: 
        Dictionary of parameters from the configuration file

    Returns:
        model name and path to sequence file
    """
    season = params["season"]
    country = params["country"]
    min_trip = params["min_trip"]
    max_trip = params["max_trip"]
    align_by_day_of_week = params["align_by_day_of_week"]
    window_hrs = params["window_hrs"]
    country_for_missing = params["country_for_missing"]

    N = params["N_samples"]
    sub_cost_method = params["sub_cost_method"]
    seq_dist_method = params["seq_dist_method"]
    n_cluster = params["n_clusters"]
    cluster_method = params["cluster_method"]

    seq_name = 'sequence_'+country+\
                          '_'+season+\
                          '_'+str(min_trip)+'d_to_'+str(max_trip)+\
                          'd_WDaligned_'+str(align_by_day_of_week).upper()+\
                          '_win_'+str(window_hrs)+\
                          '_wCtry'+str(country_for_missing).upper()

    clus_res_name = 'cluster_results_'+country+\
                          '_'+season+\
                          '_'+str(min_trip)+'d_to_'+str(max_trip)+\
                          'd_WDaligned_'+str(align_by_day_of_week).upper()+\
                          '_win_'+str(window_hrs)+\
                          '_wCtry'+str(country_for_missing).upper()+\
                          '_N_'+str(N)+\
                          '_'+sub_cost_method+\
                          '_'+seq_dist_method+\
                          '_'+cluster_method+\
                          '_NClus_'+str(n_cluster)


    seq_dir = '../../models/sequence_analysis/trained_models/'+country+'_'+season+'/'+'sequences/'
    seq_dist_dir = '../../models/sequence_analysis/trained_models/'+country+'_'+season+'/'+'sequence_distances/'
    clus_res_dir = '../../../results/sequence_analysis/'+country+'_'+season+'/'
    
    seq_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), seq_dir)
    seq_dist_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), seq_dist_dir)
    clus_res_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), clus_res_dir)


    # create necessary folders
    if not os.path.exists(seq_path):
        os.makedirs(seq_path)

    if not os.path.exists(seq_dist_path):
        os.makedirs(seq_dist_path)

    if not os.path.exists(clus_res_path):
        os.makedirs(clus_res_path)

    return os.path.join(seq_path, seq_name),clus_res_path,clus_res_name


