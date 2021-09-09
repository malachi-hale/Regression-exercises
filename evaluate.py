#Disable warnings
import warnings
warnings.filterwarnings("ignore")

#General libraries needed
import pandas as pd
import numpy as np

#Libraries for graphing
import matplotlib.pyplot as plt
import seaborn as sns

#sklearn imports
import sklearn.metrics
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_squared_error, r2_score, explained_variance_score


#Library for statistical testing and mathematics
from scipy import stats
from math import sqrt

def plot_residuals(y, yhat):
    
    residual = yhat - y
    
    plt.scatter(y, residual)
    plt.axhline(y = 0, ls = ':')
    plt.xlabel('Tips')
    plt.ylabel('Residual')
    plt.title('Linear Regression model residuals')

def regression_errors(y, yhat):
    ESS = sum((yhat - y.mean())**2)
    print('ESS', ESS)

    MSE2 = mean_squared_error(y, yhat)
    print("MSE", MSE2) 

    SSE2 = MSE2 * len(y)
    print("SSE", SSE2) 

    TSS = ESS + SSE2
    print("TSS", TSS) 

    RMSE2 = mean_squared_error(y, yhat, squared = False)
    print("RMSE", RMSE2) 

def residuals(y, yhat):
    return y - yhat

def sse(y, yhat):
    return (residuals(y, yhat) **2).sum()

def mse(y, yhat):
    n = len(y)
    return sse(y, yhat) / n

def rmse(y, yhat):
    return sqrt(mse(y, yhat))


def baseline_mean_errors(y):
    baseline = y.mean()
    
    print("MSE baseline", mse(y, baseline)) 

    print("SSE baseline", sse(y, baseline)) 

    
    print("RMSE baseline", rmse(y, baseline))  


def better_than_baseline(y, yhat):
    rmse_baseline = rmse(y, y.mean())
    rmse_model = rmse(y, yhat)

    if rmse_model < rmse_baseline:
        print("The mode performs better than baseline.")
    elif rmse_model == rmse_baseline:
        print("The model performs equal to baseline.")
    elif rmse_model > rmse_baseline:
        print("The model performs equal to baseline.")