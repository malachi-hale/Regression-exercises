import os
import pandas as pd
import env
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
import seaborn as sns
import matplotlib.pyplot as plt

#We will connect to the SQL database
def get_connection(db, user=env.user, host=env.host, password=env.password):
    '''
     We establish a connection to the SQL database, using my information stored in the env file.
    '''
    return f'mysql+pymysql://{user}:{password}@{host}/{db}'

##Now we will acquire the DataFrame
def get_telco_data():
    '''
    We will read a SQL query and create a file based on this query. I have also included a line to eliminate duplicate columns because value_counts() does not work if there are duplicate columns in the DataFrame.
    '''
    filename = "telco_churn.csv"
    ##We will write a SQL query to obtain the data
    sql = '''SELECT *
        FROM customers 
        JOIN contract_types
        ON contract_types.contract_type_id = customers.contract_type_id
        JOIN internet_service_types
        ON internet_service_types.internet_service_type_id = customers.internet_service_type_id
        JOIN payment_types 
        ON payment_types.payment_type_id = customers.payment_type_id'''
    ##If the file already exists we will simply pull the file.
    if os.path.isfile(filename):
        return pd.read_csv(filename)
    else:
        df = pd.read_sql(sql, get_connection('telco_churn'))
        ## We will get rid of duplicate columns that resulted from our SQL query
        df = df.loc[:,~df.columns.duplicated()]
        return df

#Here we acquire the DataFrame for mall customers
def get_mall_customer_data():
    '''
    We will write a SQL query to get a DataFrame for mall customers.
    '''
    filename = "mall_customers.csv"
    ##We will write a SQL query to obtain the data
    sql = '''SELECT *
        FROM customers '''
    ##If the file already exists we will simply pull the file.
    if os.path.isfile(filename):
        return pd.read_csv(filename)
    else:
        df = pd.read_sql(sql, get_connection('mall_customers'))
        return df


def split_data(df):
    #split data in train_and_validate_and_test
    train_and_validate, test = train_test_split(df, test_size=.12, random_state=123)
    #split train and validate datasets
    train, validate = train_test_split(train_and_validate, test_size=.12, random_state=123)

    return train, validate, test

def prep_telco(df):
    '''
       this function will eliminate duplicates, make dummy columns, drop redundant columns, and convert monthly charges and total charges columns into numeric.
       We will also call upon the split_data function to split our data into train, validate, and test.
    '''
        
    
    ##Add a numeric columns for churned or didn't churn
    df['has_churned'] = df['churn'].replace({'No' : 0, 'Yes': 1})
    
    ##Add a numerical column for paperless billing
    df['paperless_billing_numeric'] = df['paperless_billing'].replace({'No' : 0, 'Yes': 1})
    
    ## Now we will substitute the object values for dummy values that are easier to process. 
    dummy_df = pd.get_dummies(df[['partner', 'dependents', 'gender', 'phone_service', 'multiple_lines', 'online_security', 'online_backup', 'device_protection', 'tech_support', 'streaming_tv', 'streaming_movies']], drop_first=True)
    
    ##Concatenate our dummy values to our main Dataframe. 
    df = pd.concat([df, dummy_df], axis=1)
    
    ## Drop the redundant columns.
    df = df.drop(columns = ['gender', 'partner', 'dependents', 'phone_service', 'multiple_lines', 'online_security', 'online_backup', 'device_protection', 'tech_support', 'streaming_tv', 'streaming_movies', 'contract_type', 'internet_service_type', 'payment_type', 'churn', 'paperless_billing'])
    
    ##Our column total_charges has some empty string values, so we will replace those values with a 0
    
    df["total_charges"] = df.total_charges.replace(" ", "0")
    
    ##Now we will convert the numbers in our total_charges and monthly_charges columns to floats. 
    df['total_charges'] = df.total_charges.astype(float)
    
    df['monthly_charges'] = df.monthly_charges.astype(float)
    
    ## Now we can split our data into train, validate, and test
    
     # split data into train, validate, test dfs
    train, validate, test = split_data(df)
    
    return train, validate, test

def plot_variable_pairs(df):
        g = sns.pairplot(df, kind="reg", size = 5, corner=True, plot_kws={'line_kws':{'color':'red'}})
        return g
    
def months_to_years(df):
    df["tenure_years"] = df.tenure // 12 
    return df

def plot_categorical_and_continuous_vars(train, categorical, continuous):
    for col1 in categorical:
        for col2 in continuous:
            plt.figure(figsize=(22, 12))
            a = sns.swarmplot(x=train[col1], y=train[col2], data=train)
    for col1 in categorical:
        for col2 in continuous:
            plt.figure(figsize=(22, 12))        
            b = sns.stripplot(x=train[col1], y=train[col2], data=train)      
    for col1 in categorical:
        for col2 in continuous:
            plt.figure(figsize=(22, 12))
            c = sns.barplot(x=train[col1], y=train[col2], data=train)
    return a, b, c