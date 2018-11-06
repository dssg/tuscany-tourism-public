# coding: utf-8

# Load data based on queries by season (start time and end time)
# Created by: Orsi Vasarhelyi
# Contact: orsolya.vasarhelyi@gmail.com
# Last updated: 26.07.2018.


import sys
sys.path.append("../src/utils/")
from connect_db import db_connection

from datetime import datetime
import pandas as pd


def create_connection(username):
    """
    Create connection with tha database
    Data_creds_redshift.json.nogit should be places under /mnt/data/{username}/utils/
    """
    
    cred_location = "/mnt/data/{}/utils/data_creds_redshift.json.nogit".format(username)
    db = db_connection.DBConnection(cred_location)
    return db

def calc_season(season):
    
    """
    Input: a season (pre-summer, summer, post-summer, winter, all)
    Returns: start and end date as strings
        min_date: minimum date, in the yyyy-mm-dd hh:mm:ss format
        max_date: maximum date, in the same format
    """
    if season == 'pre-summer':
        return (str(datetime(2017, 5, 1, hour=0, minute=0, second=0)),
                str(datetime(2017, 5, 31, hour=23, minute=59, second=59)))
    elif season == "summer":
        return (str(datetime(2017, 6, 1, hour=0, minute=0, second=0)),
                str(datetime(2017, 8, 31, hour=23, minute=59, second=59)))
    elif season == "post-summer":
        return (str(datetime(2017, 9, 1, hour=0, minute=0, second=0)),
                str(datetime(2017, 10, 31, hour=23, minute=59, second=59)))
    elif season == "winter":
        return (str(datetime(2017, 11, 1, hour=0, minute=0, second=0)),
                str(datetime(2018, 2, 28, hour=23, minute=59, second=59)))
    elif season == "all":
        return (str(datetime(2017, 5, 1, hour=0, minute=0, second=0)),
                str(datetime(2018, 2, 28, hour=23, minute=59, second=59)))
    else:
        print ("Do you think {} matters? Are you not working in tourism???? You teapot!!!".format(season))
        print ("Give me a real season, choose one of these: pre-summer, summer, post-summer, winter")

def digitalize_features(df):
    """
    digitalize numeric columns for kmeans
    """
    for i in df.columns:
        if i.lower() != 'country' and i!='customer_id':
            df[i]=pd.to_numeric(df[i])
    return df


#location sequences for geo2vec
def get_location_sequences(username, country, min_date, max_date):
    """
    Run the query for location sequencess of a given country in a given time window
    
    Params:
        country: name of the country (for more details see mcc table)
        min_date: minimum date, in the yyyy-mm-dd hh:mm:ss format
        max_date: maximum date, in the same format
        
    Returns:
        df_location_sequence: feature table of a given country in a given season
    """

    db=create_connection(username)
    country=country.title()

    query=f'with get_mcc_country as  \
        (select * from tuscany.customer_feature cus  \
            join tuscany.mcc mc  \
        on mc.mcc=cus.mcc \
        where mc.country={country!r}  \
            and (cus.st_time between {min_date!r} and {max_date!r})) \
             \
    select com_locs_trunc from tuscany.customer_arrays ars \
        inner join get_mcc_country feat \
    on feat.customer_id = ars.customer_id \
    and com_locs_trunc is not null'

    df = db.sql_query_to_data_frame(query, cust_id=True)
    db.engine.dispose()
    
    return df

def get_geo2vec_data(username, season, country):
    """
    Params:
        username: to connect redshift,  
                  data_creds_redshift.json.nogit should be places under /mnt/data/{username}/utils/
        country: str, name of the country (for more details see mcc table)
        season: str, pre-summer, summer, post-summer, winter
    """
    min_date, max_date = calc_season(season)
    df = get_location_sequences(username, country, min_date, max_date)
    return df


def get_geo2vec_data_all_country(username, season):
    """
    Params:
        username: to connect redshift,  
                  data_creds_redshift.json.nogit should be places under /mnt/data/{username}/utils/
        country: str, name of the country (for more details see mcc table)
        season: str, pre-summer, summer, post-summer, winter
    """
    min_date, max_date = calc_season(season)
    db=create_connection(username)

    query=f'with get_mcc_country as  \
        (select * from tuscany.customer_feature cus  \
         where (cus.st_time between {min_date!r} and {max_date!r})) \
             \
        select com_locs_trunc from tuscany.customer_arrays ars \
        inner join get_mcc_country feat \
        on feat.customer_id = ars.customer_id \
        and com_locs_trunc is not null'

    df = db.sql_query_to_data_frame(query, cust_id=True)
    db.engine.dispose()
        
    return df

#customer arrays for sequences
def get_customer_arrays(username, country, min_date, max_date, min_trip, max_trip):
    """
    Run the query for customer arrays of a given country in a given time window
    
    Params:
        country: name of the country (for more details see mcc table), 
            et country = "all:" means all countries
        min_date: minimum date, in the yyyy-mm-dd hh:mm:ss format
        max_date: maximum date, in the same format
        min_trip: int, filter for customers with the given minimum length of trip duration in Italy
        max_trip: int, filter for customers with the given maximum length of trip duration in Italy
        
    Returns:
        df_location_sequence: feature table of a given country in a given season
    """

    db=create_connection(username)
    country=country.title()

    query=f'select  \
        ars.customer_nr,  \
        ars.com_locs_new as locations,  \
        ars.times_new as times,  \
        ars.st_time,  \
        ars.en_time,  \
        ars.mcc  \
        from tuscany.customer_arrays ars  \
        where  ars.trip_duration <= {max_trip!r}  \
        and ars.trip_duration > {min_trip!r}  \
        and times_new is not null  \
        and (st_time between {min_date!r} and {max_date!r})  \
        and mcc in (select mcc from tuscany.mcc mc  \
        where mc.country={country!r})'
    
    df = db.sql_query_to_data_frame(query, cust_id=False)
    db.engine.dispose()
    return df

def get_sequence_data(username, season, country, min_trip, max_trip):
    """
    Params:
        username: to connect redshift,  
                  data_creds_redshift.json.nogit should be places under /mnt/data/{username}/utils/
        country: str, name of the country (for more details see mcc table)
        season: str, pre-summer, summer, post-summer, winter
    """
    min_date, max_date = calc_season(season)
    df = get_customer_arrays(username, country, min_date, max_date, min_trip, max_trip)
    return df

#customer features for kmeans
def get_customer_features(username, country, min_date, max_date):
    """
    Run the query for customer features of a given country in a given time window
    
    Params:
        country: name of the country (for more details see mcc table)
        min_date: minimum date, in the yyyy-mm-dd hh:mm:ss format
        max_date: maximum date, in the same format
        
    Returns:
        df_location_sequence: feature table of a given country in a given season
    """
    
    db=create_connection(username)
    country=country.title()

    query=f'select * from tuscany.customer_feature cus  \
                join tuscany.mcc mc  \
            on mc.mcc=cus.mcc  \
            where mc.country={country!r}  \
                and (cus.st_time between {min_date!r} and {max_date!r})  \
                and cus.customer_id not in (select customer_id from tuscany.excluded_customers)'

    df = db.sql_query_to_data_frame(query, cust_id=True)
    df2 = digitalize_features(df)
    return df2


def get_k_means_data(username, season, country):
    """
    Params:
        username: to connect redshift,  
                  data_creds_redshift.json.nogit should be places under /mnt/data/{username}/utils/
        country: str, name of the country (for more details see mcc table)
        season: str, pre-summer, summer, post-summer, winter
    """
    min_date, max_date = calc_season(season)
    df = get_customer_features(username, country, min_date, max_date)
    df2 = digitalize_features(df)
    return df2

def get_k_means_data_for_all_countries(username, season):
    """ 
    Uset his function to get k-means data for all countries
    Params:
        username: to connect redshift,  
                  data_creds_redshift.json.nogit should be places under /mnt/data/{username}/utils/
        season: str, pre-summer, summer, post-summer, winter
    """
    min_date, max_date = calc_season(season)
    db=create_connection(username)
    query=f'select * from tuscany.customer_feature cus  \
                join tuscany.mcc mc  \
            on mc.mcc=cus.mcc  \
                and (cus.st_time between {min_date!r} and {max_date!r})  \
                and cus.customer_id not in (select customer_id from tuscany.excluded_customers)'
    df = db.sql_query_to_data_frame(query, cust_id=True)
    db.engine.dispose()
    df2 = digitalize_features(df)
    return df2








