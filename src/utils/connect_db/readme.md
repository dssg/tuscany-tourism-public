## Database Connection - Requirements

1) Create a file with the following information:
```
{
  "user_name": "YOUR_DB_USER_NAME",
  "password": "YOUR_DB_PASSWORD",
  "host_name": "YOUR_HOST_NAME.redshift.amazonaws.com",
  "port_num": "YOUR_PORT_NUMBER",
  "db_name": "YOUR_CB_NAME"
}
```
Be sure to modify the host_name or port_num in case you are not connecting to
the dwh.

2) Name the file something like ```redshift_creds.json.nogit```


## Using the Database Connection - Jupyter Notebook

1) Import the library:
```python
import sys
sys.path.append("..")
from connect_db import db_connection
```

2) Create a connection:
```python
# Start database connection
YOURNAME = your_redshift_user_name
cred_location = '/Users/YOURNAME/utils/data_creds_redshift.json.nogit'
db = db_connection.DBConnection(cred_location)

```

3) Now, you are ready to query the db by calling either

```python
# This will return a pandas data frame with the results
df = db.sql_query_to_data_frame(query, cust_id=True)
```
This takes a ```query``` (string) and returns a Pandas Data Frame with the results.

cust_id: boolean, 
 	True: if the df contains the customer_id and customer_nr too, function drops the customer_id to save memory.
    False: function does not drop customer_id, use this when you want to keep customer_id as a string or the df does not contain it.

Please note:
Connection method has been optimized to use less memory based on this article: http://dev.mobify.com/blog/sqlalchemy-memory-magic/
