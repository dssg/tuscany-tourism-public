import json
import os
import pickle

import pandas as pd
import sqlalchemy

class StringFolder(object):
    """
    Class that will fold strings. See 'fold_string'.
    This object may be safely deleted or go out of scope when
    strings have been folded.
    """
    def __init__(self):
        self.unicode_map = {}

    def fold_string(self, s):
        """
        Given a string (or unicode) parameter s, return a string object
        that has the same value as s (and may be s). For all objects
        with a given value, the same object will be returned. For unicode
        objects that can be coerced to a string with the same value, a
        string object will be returned.
        If s is not a string or unicode object, it is returned unchanged.
        :param s: a string or unicode object.
        :return: a string or unicode object.
        """
        # If s is not a string or unicode object, return it unchanged
        if not isinstance(s, str):
            return s

        # If s is already a string, then str() has no effect.
        # If s is Unicode, try and encode as a string and use intern.
        # If s is Unicode and can't be encoded as a string, this try
        # will raise a UnicodeEncodeError.
        try:
            return str(s)
        except UnicodeEncodeError:
            # Fall through and handle s as Unicode
            pass

        # Look up the unicode value in the map and return
        # the object from the map. If there is no matching entry,
        # store this unicode object in the map and return it.
        t = self.unicode_map.get(s, None)
        if t is None:
            # Put s in the map
            t = self.unicode_map[s] = s
        return t


def string_folding_wrapper(results):
    keys = results.keys()
    folder = StringFolder()
    for row in results:
        yield tuple(folder.fold_string(row[key]) for key in keys)




class DBConnection:
    """
    Class that create connection to the DB
    """

    def __init__(self, cred_location):
        self.cred_location = cred_location
        self.engine = self.create_engine()

    def create_engine(self):
        with open(self.cred_location) as fh:
            creds = json.loads(fh.read())

        db_connection = 'postgresql://' + \
                        creds['user_name'] + ':' + creds['password'] + '@' + \
                        creds['host_name'] + ':' + creds['port_num'] + '/' + creds['db_name']

        engine = sqlalchemy.create_engine(db_connection)

        return engine
    
        
    def sql_query_to_data_frame(self, query, cust_id):
        """return a dataframe based ona query
        query: SQL query as a string, without a ; in the end
        cust_id: boolean, 
            True means the dataframe contains the customer_id and
            customer_nr too, and code drops the customer_id to save
            memory.
            False: it does not drop customer_id 
        """

        query = query.replace("%", "%%")

        # connection is closed exiting the with

        with self.engine.begin() as connection:
            results = (connection.execution_options(stream_results=True).execute(query))
            df = pd.DataFrame(string_folding_wrapper(results))
            df.columns = results.keys()
            df = df.iloc[:, ~df.columns.duplicated()]
            if 'customer_id' in df.columns and cust_id==True:
                df=df.drop(columns=['customer_id'])
        #connection.close()
        self.engine.dispose()
        return df


    def load_and_save_data_frame(self, filename, query, overwrite=False):

        # Check if the directory exists, otherwise create
        dir_name = os.path.dirname(filename)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

        if os.path.isfile(filename) and os.stat(filename).st_size > 0 and not overwrite:
            with open(filename, 'r') as file:
                df = pickle.load(file)
        else:
            with open(filename, 'w') as file:
                df = self.sql_query_to_data_frame(query)
                pickle.dump(df, file)

        return df