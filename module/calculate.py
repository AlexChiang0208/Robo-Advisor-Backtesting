import pandas as pd
import numpy as np
import scipy.optimize as sco

from module.data import Data
twStock, TWII, ret1_twStock, ret1_TWII, ret240_twStock, ret240_TWII = Data()

# alpha
def get_alpha(stock_id, trade_date, period):
    
    feature = []
    for j in ret1_twStock[stock_id]:
        X = ret1_TWII.loc[:trade_date].iloc[-period:]['^TWII']
        Y = ret1_twStock[stock_id].loc[:trade_date].iloc[-period:][j]
        X_bar = np.mean(X)
        Y_bar = np.mean(Y)
        b1 = np.dot((X-X_bar), (Y-Y_bar)) / np.square((X-X_bar)).sum()
        b0 = Y_bar - b1 * X_bar
        feature.append(b0)
        
    feature = pd.DataFrame({'feature':feature}, index = stock_id)
    return feature

# beta
def get_beta(stock_id, trade_date, period):

    feature = []
    for j in ret1_twStock[stock_id]:
        X = ret1_TWII.loc[:trade_date].iloc[-period:]['^TWII']
        Y = ret1_twStock[stock_id].loc[:trade_date].iloc[-period:][j]
        X_bar = np.mean(X)
        Y_bar = np.mean(Y)
        b1 = np.dot((X-X_bar), (Y-Y_bar)) / np.square((X-X_bar)).sum()
        feature.append(b1)
    
    feature = pd.DataFrame({'feature':feature}, index = stock_id)
    return feature

# skew1
def get_skew1(stock_id, trade_date, period):
    
    feature = ret1_twStock[stock_id].rolling(period).skew().loc[trade_date].to_frame()
    feature.columns = ['feature']
    return feature

# skew2
def get_skew2(stock_id, trade_date, period):
    
    feature = ret240_twStock[stock_id].rolling(period).skew().loc[trade_date].to_frame()
    feature.columns = ['feature']
    return feature


# Markowitz's MV model
def Portfolio_volatility(weights, mean_returns, cov_matrix):
    returns = np.sum(mean_returns * weights)
    std = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))    
    return std

def min_variance(mean_returns, cov_matrix, k):
    num_assets = len(mean_returns)
    args = (mean_returns, cov_matrix)
    constraints = ({'type':'eq', 'fun': lambda x: np.sum(x) - 1})
    bound = (0,k) ## Max percentage
    bounds = tuple(bound for asset in range(num_assets))
    
    result = sco.minimize(Portfolio_volatility, num_assets*[1/num_assets], args=args, method='SLSQP', bounds=bounds, constraints=constraints)
    return result


#####################
# # alpha
# def get_alpha(trade_date, period):
    
#     feature = []
#     for j in ret1_TW150:
#         X = ret1_TWII.loc[:trade_date].iloc[-period:]['^TWII']
#         Y = ret1_TW150.loc[:trade_date].iloc[-period:][j]
#         X_bar = np.mean(X)
#         Y_bar = np.mean(Y)
#         b1 = np.dot((X-X_bar), (Y-Y_bar)) / np.square((X-X_bar)).sum()
#         b0 = Y_bar - b1 * X_bar
#         feature.append(b0)
        
#     feature = pd.DataFrame({'feature':feature}, index=list(ret1_TW150.columns))
#     return feature

# # beta
# def get_beta(trade_date, period):

#     feature = []
#     for j in ret1_TW150:
#         X = ret1_TWII.loc[:trade_date].iloc[-period:]['^TWII']
#         Y = ret1_TW150.loc[:trade_date].iloc[-period:][j]
#         X_bar = np.mean(X)
#         Y_bar = np.mean(Y)
#         b1 = np.dot((X-X_bar), (Y-Y_bar)) / np.square((X-X_bar)).sum()
#         feature.append(b1)
    
#     feature = pd.DataFrame({'feature':feature}, index=list(ret1_TW150.columns))
#     return feature

# # skew1
# def get_skew1(trade_date, period):
    
#     feature = ret1_TW150.rolling(period).skew().loc[trade_date].to_frame()
#     feature.columns = ['feature']
#     return feature

# # skew2
# def get_skew2(trade_date, period):
    
#     feature = ret240_TW150.rolling(period).skew().loc[trade_date].to_frame()
#     feature.columns = ['feature']
#     return feature


# # Markowitz's MV model
# def Portfolio_volatility(weights, mean_returns, cov_matrix):
#     returns = np.sum(mean_returns * weights)
#     std = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))    
#     return std

# def min_variance(mean_returns, cov_matrix, k):
#     num_assets = len(mean_returns)
#     args = (mean_returns, cov_matrix)
#     constraints = ({'type':'eq', 'fun': lambda x: np.sum(x) - 1})
#     bound = (0,k) ## Max percentage
#     bounds = tuple(bound for asset in range(num_assets))
    
#     result = sco.minimize(Portfolio_volatility, num_assets*[1/num_assets], args=args, method='SLSQP', bounds=bounds, constraints=constraints)
#     return result
