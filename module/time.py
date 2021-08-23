import pandas as pd
import datetime

from module.data import Data
twStock, TWII, ret1_twStock, ret1_TWII, ret240_twStock, ret240_TWII = Data()

# 計算 start_day 的「前一天」
def the_day_before(date):

    date = pd.to_datetime(date)
    feature_day = date - datetime.timedelta(days=1)
    while True:
        if feature_day in twStock.index:
            break
        else:
            feature_day = feature_day - datetime.timedelta(days=1)    
    return feature_day

# 計算 start_day 的「後一天」
def the_day_after(date):

    start_day = date + datetime.timedelta(days=1)
    while True:
        if start_day in twStock.index:
            break
        elif start_day == twStock.index[-1] + datetime.timedelta(days=1):
            start_day = start_day - datetime.timedelta(days=1)
            break
        else:
            start_day = start_day + datetime.timedelta(days=1)    
    return start_day

# 找出真正交易的第一天
def real_start_day(date):

    start_day = pd.to_datetime(date)
    while True:
        if start_day in twStock.index:
            break
        else:
            start_day = start_day + datetime.timedelta(days=1)    
    return start_day

# 找出真正結束的那一天
def real_end_day(date):
   
    end_day = pd.to_datetime(date)
    while True:
        if end_day in twStock.index:
            break
        else:
            end_day = end_day - datetime.timedelta(days=1)    
    return end_day
