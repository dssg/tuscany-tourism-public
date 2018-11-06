import sys
sys.path.append("..")
from new_codebase.dev.connect_db import db_connection


username='ovasarhelyi'

cred_location = '/mnt/data/'+username+'/TPT_tourism/connect_db/data_creds.json.nogit'
db = db_connection.DBConnection(cred_location)

query="""select 
mcc, 
count(distinct customer_id) as num_unique_cus
from
tuscany.vodafone
group by mcc
order by num_unique_cus desc"""

number_of_cus_per_country= db.sql_query_to_data_frame(query)

number_of_cus_per_country.to_csv("/mnt/data/shared/number_of_cus_per_country.csv")