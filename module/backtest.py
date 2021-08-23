import pandas as pd
import numpy as np
import os

from module.data import Data
from module.time import real_start_day
from module.calculate import *

path = os.getcwd()
twScale = pd.read_csv(path + '/dataset/twScale.csv', parse_dates=True, index_col='Date')
twStock, TWII, ret1_twStock, ret1_TWII, ret240_twStock, ret240_TWII = Data()

### test
# TW150 = pd.read_csv(path + '/dataset/TW150_CloseAdj.csv', parse_dates=True, index_col='Date')
# stock_id = TW150.columns

class Backtest:

    def __init__(self, beginning_money = 100,
                 start_day = '2006-01-01', 
                 scale_select = 'max',
                 scale_num = 150,
                 strategy = 'alpha',
                 feature_select = 'max',
                 feature_period = 240, 
                 stock_num = 5, 
                 max_percentage = 0.2, 
                 rebalance = 240, 
                 dynamic_rebalance = False, 
                 stop_loss = 0.3):
        
        '''
        < 參數介紹 >
        beginning_money
        預設起始金額 100 元
        
        start_day
        預設為 '2006-01-01'
        需設定在 2006 年之後  
        
        scale_select = ['max', 'min']
        預設為 max
        * max 選取市值最大者
        * min 選取市值最小者        
        
        scale_num
        預設為 150
        以市值排名數量作為股票池
        
        strategy = ['alpha', 'beta', 'skew1', 'skew2']
        預設為 alpha
        * skew1 每日報酬率計算的偏態
        * skew2 每年報酬率計算的偏態
        
        feature_select = ['max', 'min']
        預設為 max
        * max 選取參數最大者
        * min 選取參數最小者
        
        feature_period
        預設為 240
        參數取自多長的時間，最多 240
        (建議不少於 60 天)
        
        stock_num
        預設為 5
        投資組合有幾檔股票
        (建議以 3 5 8 10 為主)
        
        max_percentage
        預設為 0.2
        每一檔股票的最大權重
        最小為 1 / stock_num
        最大為 1
        
        rebalance
        預設 240
        多少天靜態再平衡
        （若設定 10000，將不會有靜態平衡的條件）
        
        dynamic_rebalance = [True, False]
        預設為 False
        是否做停損再平衡
        
        stop_loss
        預設為 0.3
        若 dynamic_rebalance = True
        才會執行此條件
        (建議 0.2 ~ 0.4)
        '''
        
        # 定義傳入值屬性
        self.beginning_money = beginning_money
        self.strategy = strategy
        self.start_day = start_day
        
        # Benchmark
        TWII_ret = TWII.loc[self.start_day:].pct_change()
        TWII_ret.iloc[0] = 0
        TWII_ret += 1
        self.benchmark = TWII_ret.cumprod() * 100
        self.benchmark.columns = ['benchmark']
        
        # 交易起始日
        self.start_day = real_start_day(date = self.start_day)
        
        # Portfolio
        self.portfolio = pd.DataFrame()
        stop_loss_day = self.start_day
        
        while self.start_day != twStock.index[-1]:
        
            # 移除重複出現的日期
            self.portfolio = self.portfolio.iloc[:-1]
            
            # 股票池：stock_id
            if strategy == 'skew2':
                scale_rank = pd.concat([twScale.loc[:self.start_day].iloc[-(feature_period*2+1):], 
                                        twScale.loc[self.start_day:].iloc[1:rebalance+1]]).dropna(axis = 1).loc[self.start_day]
            else:
                scale_rank = pd.concat([twScale.loc[:self.start_day].iloc[-(feature_period+1):], 
                                        twScale.loc[self.start_day:].iloc[1:rebalance+1]]).dropna(axis = 1).loc[self.start_day]
            if scale_select == 'max':
                stock_id = scale_rank.sort_values(ascending = False)[:scale_num].index
            elif scale_select == 'min':
                stock_id = scale_rank.sort_values(ascending = True)[:scale_num].index

            # 挑選投資標的
            feature = globals()['get_' + self.strategy](stock_id = stock_id, trade_date = self.start_day, 
                                                        period = feature_period)
            
            if feature_select == 'max':
                buy_stock = feature.sort_values(by = 'feature', 
                                                ascending=False).head(stock_num).index
            elif feature_select == 'min':
                buy_stock = feature.sort_values(by = 'feature', 
                                                ascending=True).head(stock_num).index                
            
            # 計算投資權重
            mean_return = ret1_twStock[stock_id].loc[:self.start_day].iloc[-240:][buy_stock].mean()
            cov_matrix = ret1_twStock[stock_id].loc[:self.start_day].iloc[-240:][buy_stock].cov()
            w = min_variance(mean_return, cov_matrix, k = max_percentage)['x']
            
            # 投資組合的總資產
            portfolio_once = pd.DataFrame()
            
            for i in range(len(w)):
                each_w = self.beginning_money * w[i]
                each_one = twStock[stock_id][buy_stock[i]].loc[self.start_day:].iloc[:rebalance]
                each_ret = each_one.pct_change()
                each_ret.iloc[0] = 0
                each_ret += 1
                each_earn = (each_ret.cumprod() * each_w).to_frame()
                portfolio_once = pd.concat([portfolio_once, each_earn], axis = 1)
            
            portfolio_once = portfolio_once.sum(axis = 1).to_frame() 
            self.portfolio = pd.concat([self.portfolio, portfolio_once], axis = 0)
        
            # 設置停損點
            if dynamic_rebalance == True:
                self.max_drawdown = (self.portfolio.loc[stop_loss_day:] / self.portfolio.loc[stop_loss_day:].rolling(min_periods = 1, window = 240).max()) - 1
                if len(self.max_drawdown[self.max_drawdown.loc[:,0] < -stop_loss]) != 0:
                    stop_loss_day = self.max_drawdown[self.max_drawdown.loc[:,0] < -stop_loss].iloc[0].name
                    self.portfolio = self.portfolio.loc[:stop_loss_day]
                
            self.start_day = self.portfolio.index[-1]  
            self.beginning_money = self.portfolio.iloc[-1,0]
        
        self.portfolio.columns = ['portfolio']
        self.max_drawdown = (self.portfolio / self.portfolio.rolling(min_periods = 1, window = 240).max()) - 1
        self.portfolio_benchmark = pd.concat([self.portfolio, self.benchmark], axis = 1)
        

    def show_portfolio(self):
        self.portfolio_benchmark.plot(grid = True, title = self.strategy+'_strategy', figsize=(16, 6))
        self.max_drawdown.plot.area(stacked=False, color = 'red', title = self.strategy+'_drawdown', legend=False, figsize=(16, 6))
        return 


    def show_index(self, index):
        
        '''
        Financial Index:
        (1)Max_drawdown
        (2)Accumulation_return
        (3)Annual_return
        (4)Annual_volatility
        (5)Neg_annual_volatility
        (6)Sharpe_ratio
        (7)Sortino_ratio
        (8)Calmar_ratio
        (9)All
        ''' 
        
        day_of_year = int(len(twStock.loc['2006-01-02':'2020-12-31'].index) / 15)
        total_days = len(self.portfolio.index)
        total_years = total_days / day_of_year
        portfolio_ret = self.portfolio.pct_change().dropna()
        bench_ret = self.benchmark.pct_change().dropna()
        bench_MDD = (self.benchmark / self.benchmark.rolling(min_periods = 1, window = 240).max()) - 1
        
        # 計算 Financial Index
        Max_drawdown = abs(self.max_drawdown.min())[0]
        Accumulation_return = ((self.portfolio.iloc[-1] - self.portfolio.iloc[0]) / self.portfolio.iloc[0])[0]
        Annual_return = ((self.portfolio.iloc[-1] / self.portfolio.iloc[0])**(1/total_years) - 1)[0]
        Annual_volatility = (portfolio_ret.std() * np.sqrt(day_of_year))[0]
        Neg_annual_volatility = (portfolio_ret.applymap(lambda x: 0 if x > 0 else x).std() * np.sqrt(day_of_year))[0]
        Sharpe_ratio = Annual_return / Annual_volatility
        Sortino_ratio = Annual_return / Neg_annual_volatility
        Calmar_ratio = Annual_return / Max_drawdown
        
        # 計算 Financial Index (Benchmark)
        B_Max_drawdown = abs(bench_MDD.min())[0]
        B_Accumulation_return = ((self.benchmark.iloc[-1] - self.benchmark.iloc[0]) / self.benchmark.iloc[0])[0]
        B_Annual_return = ((self.benchmark.iloc[-1] / self.benchmark.iloc[0])**(1/total_years) - 1)[0]
        B_Annual_volatility = (bench_ret.std() * np.sqrt(day_of_year))[0]
        B_Neg_annual_volatility = (bench_ret.applymap(lambda x: 0 if x > 0 else x).std() * np.sqrt(day_of_year))[0]
        B_Sharpe_ratio = B_Annual_return / B_Annual_volatility
        B_Sortino_ratio = B_Annual_return / B_Neg_annual_volatility
        B_Calmar_ratio = B_Annual_return / B_Max_drawdown
        
        if index == 'All':
            return print(' <Strategy> \n','Max_drawdown:',np.round(Max_drawdown, 4), '\n',
                     'Accumulation_return:',np.round(Accumulation_return, 4), '\n',
                     'Annual_return:',np.round(Annual_return, 4), '\n',
                     'Annual_volatility:',np.round(Annual_volatility, 4), '\n',
                     'Neg_annual_volatility:',np.round(Neg_annual_volatility, 4), '\n',
                     'Sharpe_ratio:',np.round(Sharpe_ratio, 4), '\n',
                     'Sortino_ratio:',np.round(Sortino_ratio, 4), '\n',
                     'Calmar_ratio:',np.round(Calmar_ratio, 4),
                     '\n \n <Benchmark> \n', 'Max_drawdown:',np.round(B_Max_drawdown, 4), '\n',
                     'Accumulation_return:',np.round(B_Accumulation_return, 4), '\n',
                     'Annual_return:',np.round(B_Annual_return, 4), '\n',
                     'Annual_volatility:',np.round(B_Annual_volatility, 4), '\n',
                     'Neg_annual_volatility:',np.round(B_Neg_annual_volatility, 4), '\n',
                     'Sharpe_ratio:',np.round(B_Sharpe_ratio, 4), '\n',
                     'Sortino_ratio:',np.round(B_Sortino_ratio, 4), '\n',
                     'Calmar_ratio:',np.round(B_Calmar_ratio, 4))
        else:
            return print(' <Strategy> \n',index, ':', np.round(eval(index),4),
                        '\n \n <Benchmark> \n',index, ':', np.round(eval('B_'+index),4))
