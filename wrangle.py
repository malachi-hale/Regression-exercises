#Disable warnings
import warnings
warnings.filterwarnings("ignore")

#Libraries for processing data
import pandas as pd
import numpy as np

#Import libraries for graphing
import matplotlib.pyplot as plt
import seaborn as sns

#Libraries for obtaining data from SQL databse
import env
import os

#Library for dealing with NA values
from sklearn.impute import SimpleImputer

#First we establish a connection to the SQL server
def get_connection(db, user=env.user, host=env.host, password=env.password):
    '''
     We establish a connection to the SQL database, using my information stored in the env file.
    '''
    return f'mysql+pymysql://{user}:{password}@{host}/{db}'

#Now we will make our DataFrame with the relevant Zillow data
def get_zillow_data():
    '''
    We will read a SQL query and create a file based on this query. I have also included a line to eliminate duplicate columns because value_counts() does not work if there are duplicate columns in the DataFrame.
    '''
    filename = "zillow.csv"
    ##We will write a SQL query to obtain the data
    sql = ''' 
    SELECT bedroomcnt, bathroomcnt, calculatedfinishedsquarefeet,
         taxvaluedollarcnt, yearbuilt, taxamount, fips from properties_2017
    JOIN propertylandusetype
    ON propertylandusetype.propertylandusetypeid = properties_2017.propertylandusetypeid
    AND propertylandusetype.propertylandusetypeid = 261 
    '''
    ##If the file already exists we will simply pull the file.
    if os.path.isfile(filename):
        return pd.read_csv(filename)
    else:
        df = pd.read_sql(sql, get_connection('zillow'))
        return df

#Now we will replace the null values with the mean value of each column
def impute_null_values():
    '''
    We will use SimpleImputer to impute the mean value into the null values into each column.
    '''
    #We will use the mean imputer function.
    imputer = SimpleImputer(strategy='mean')

    #We will create a for loop that will impute all the null values in each one of our columns.
    for col in df.columns:
        df[[col]] = imputer.fit_transform(df[[col]])
    return df