import pandas as pd
import sqlite3
from functools import reduce
#merge function:
def merge_df(list_df, column):
    return reduce(lambda left, right: pd.merge(left, right, on=column), list_df)
def adquisition(df):
    # Create the connection with my downloaded data base
    cnx = sqlite3.connect('/home/luana/IRONHACK/Ironhack-Module-1-Project/data/luanasolis.db')
    # create the dataframe from a query
    df_business = pd.read_sql_query("SELECT * FROM business_info", cnx)
    df_rank = pd.read_sql_query("SELECT * FROM rank_info", cnx)
    df_personal = pd.read_sql_query("SELECT * FROM personal_info", cnx)
    # function for data adquisition:
    dfs = [df_business, df_rank, df_personal]
    # given data base
    df = merge_df(dfs, 'id')
    return df
adquisition('df')
