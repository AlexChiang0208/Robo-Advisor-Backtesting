import pandas as pd
import numpy as np
import scipy.optimize as sco
import statsmodels.api as sm

from module.data import Data
TW150, TWII, ret1_TW150, ret1_TWII, ret240_TW150, ret240_TWII, stock_name = Data()


# alpha
def get_alpha(trade_date, period):
    
    feature = []
    
    for j in ret1_TW150:
        XX = sm.add_constant(ret1_TWII.loc[:trade_date].iloc[-period:])
        est = sm.OLS(ret1_TW150.loc[:trade_date].iloc[-period:][j], np.array(XX), missing='drop')
        est = est.fit()
        feature.append(est.params[0])
    
    feature = pd.DataFrame({'feature':feature}, index=list(ret1_TW150.columns))
    return feature

# beta
def get_beta(trade_date, period):

    feature = []

    for j in ret1_TW150:
        XX = sm.add_constant(ret1_TWII.loc[:trade_date].iloc[-period:])
        est = sm.OLS(ret1_TW150.loc[:trade_date].iloc[-period:][j], np.array(XX), missing='drop')
        est = est.fit()
        feature.append(est.params[1])
    
    feature = pd.DataFrame({'feature':feature}, index=list(ret1_TW150.columns))
    return feature

# skew1
def get_skew1(trade_date, period):
    
    feature = ret1_TW150.rolling(period).skew().loc[trade_date].to_frame()
    feature.columns = ['feature']
    return feature

# skew2
def get_skew2(trade_date, period):
    
    feature = ret240_TW150.rolling(period).skew().loc[trade_date].to_frame()
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
