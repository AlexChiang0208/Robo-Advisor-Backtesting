import pandas as pd
import numpy as np
import os

def Data():

    # 確認路徑
    path = os.getcwd()

    # 取出原始資料（無缺漏值的兩組 csv 檔－ TWII 與 TW150）
    TW150 = pd.read_csv(path + '/dataset/TW150_CloseAdj.csv', parse_dates=True, index_col='Date')
    TWII = pd.read_csv(path + '/dataset/TWII_CloseAdj.csv', parse_dates=True, index_col='Date')
    stock_name = TW150.columns
    
    # 計算兩種報酬率
    ret1_TW150 = np.log(TW150/TW150.shift(1)).dropna() * 240
    ret1_TWII = np.log(TWII/TWII.shift(1)).dropna() * 240
    ret240_TW150 = np.log(TW150/TW150.shift(240)).dropna()
    ret240_TWII = np.log(TWII/TWII.shift(240)).dropna()
    
    return TW150, TWII, ret1_TW150, ret1_TWII, ret240_TW150, ret240_TWII, stock_name
