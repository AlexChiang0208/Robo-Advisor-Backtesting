# 單因子策略 理財機器人回測

作者：江祐宏 Alex Chiang

背景：東吳大學 財務工程與精算數學系 大四

更新日期：2021/8/23

---

## 專案簡介
更嚴謹的驗證之前所做的研究：(1)採用 TEJ Pro 專業資料庫之 1971 ~ 2021/8/20 的調整後收盤價 (2)以即時的市值先篩選出「市值前 N 大」的股票池

#### 實驗架構：
1. 依照即時市值篩選出股票池
2. 單因子選股－CAMP 模型的 alpha, beta 指標；資產報酬率的偏態係數
3. 投資組合最佳化－Markowitz 均異最適化模型
4. 定期再平衡
5. 停損再平衡

## 使用方法
下載此 repository，安裝相關套件後可直接於 jupyter notebook 執行 [主程式](main.ipynb)。

* [主程式執行環境需求](requirements.txt)
* Python 版本：3.7.4

## 程式使用說明

```python
Backtest(beginning_money = 100,
         start_day = '1973-01-01', 
         scale_select = 'max',
         scale_num = 100,
         strategy = 'alpha',
         feature_select = 'max',
         feature_period = 240, 
         stock_num = 10, 
         max_percentage = 0.12, 
         rebalance = 60, 
         dynamic_rebalance = False, 
         stop_loss = 0.3)
```

**(1) beginning_money**

`起始金額為多少錢（預設為 100）`

**(2) start_day**

`從哪一天開始交易（預設為 2006/1/1）`

> 註：需設定在 2006 年之後  

**(3) scale_select** = ['max', 'min']

`選取「市值大」或「市值小」（預設為 max）`


**(4) scale_num**

`篩選市值 N 檔內範圍的股票`

**(5) strategy** = ['alpha', 'beta', 'skew1', 'skew2']

`使用哪一個因子作為選股方法`

* alpha: CAPM 模型之截距項
* beta: CAPM 模型之斜率項
* skew1: 每日報酬率計算的偏態
* skew2: 每年報酬率計算的偏態

> 註：策略因子可於 [套件模組](module/calculate.py) 中自行調整


**(6) feature_select** = ['max', 'min']

`選取該因子最大項或最小項為選股標準`

**(7) feature_period** 

`策略因子取自多長的時間製作（預設為 240）`

> 註：建議不少於 60。當超過 240 的 n 天，start_day 需向後 n 個交易日才可執行（不然算不出早期的策略因子，會導致執行失敗）

**(8) stock_num**

`每次將幾檔股票放入投資組合（預設為 5）`

> 註：建議以 3 5 8 10 為主

**(9) max_percentage** 

`每一檔股票的最大配置比重（預設為 0.2）`

> 註：最小必須為 1 / n_stock；最大為 1

**(10) rebalance** 

`幾個交易日做一次靜態再平衡（預設 240）`

> 註：若設定 10000，將不會有靜態平衡的條件

**(11) dynamic_rebalance** = [True, False] 

`是否做停損再平衡（預設為 False）`

**(12) stop_loss** 

`設置停損百分比（預設為 0.3）`

> 註：當 dynamic_rebalance = True，才會執行此條件
