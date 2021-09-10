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

from sklearn.model_selection import train_test_split

#Library needed for scaling the data
import sklearn.preprocessing

def split_data(df):
    #split data in train_and_validate_and_test
    train_and_validate, test = train_test_split(df, test_size=.12, random_state=123)
    #split train and validate datasets
    train, validate = train_test_split(train_and_validate, test_size=.12, random_state=123)

    return train, validate, test

def add_scaled_columns(train, validate, test):
    columns_to_scale = ['calculatedfinishedsquarefeet', 'bedroomcnt', 'bathroomcnt']
    # new column names
    new_column_names = [c + '_scaled' for c in columns_to_scale]
    
    #Define scaler
    scaler_min_max = sklearn.preprocessing.MinMaxScaler()
    
    # Fit the scaler on the train
    scaler_min_max.fit(train[columns_to_scale])
    
    # transform train validate and test
    train = pd.concat([
        train,
        pd.DataFrame(scaler_min_max.transform(train[columns_to_scale]), columns=new_column_names, index=train.index),
    ], axis=1)
    
    validate = pd.concat([
        validate,
        pd.DataFrame(scaler_min_max.transform(validate[columns_to_scale]), columns=new_column_names, index=validate.index),
    ], axis=1)
    
    
    test = pd.concat([
        test,
        pd.DataFrame(scaler_min_max.transform(test[columns_to_scale]), columns=new_column_names, index=test.index),
    ], axis=1)
    
    return train, validate, test

