# This file has a python script to load the location dictionary table 
# from postgres and save as a csv to copy into redshift

# Importing libraries
import sys
sys.path.append("..")
from new_codebase.dev.connect_db import db_connection

# Connecting to database
# Change location of credentials to connect to the database
username='kmohan'
cred_location = '/mnt/data/'+username+'/utils/data_creds_postgres.json.nogit'
db = db_connection.DBConnection(cred_location)

#  Querying the location_dictionary table from postgres 
query = """select * from tuscany.location_dictionary"""

# Load table into pandas dataframe
df_loc_dict = db.sql_query_to_data_frame(query, cust_id=True)

# Save dataframe as csv to load into redshift
df_loc_dict.to_csv('/mnt/data/kmohan/location_dictionary.csv',sep=';',index=False)

# NOTE: The csv file needs to be s3 in order to copy onto redshift