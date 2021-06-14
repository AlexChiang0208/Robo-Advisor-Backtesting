# 單因子策略 理財機器人回測

## 簡介
將 2004~2020 年台灣市值前 150 大的股票（刪除早期未上市及下市股票，共 108 檔）與台灣加權股價指數之調整後收盤價做一個簡易回測系統，實證機器人理財的可行性。

#### 理財機器人架構：
1. 單因子選股－CAMP 模型的 alpha, beta 指標；資產報酬率的偏態係數
2. 投資組合最佳化－Markowitz 均異最適化模型
3. 定期再平衡
4. 停損再平衡

## 使用方法
下載此 repository，安裝相關套件後可直接於 jupyter notebook 執行 [主程式](main.ipynb)。

[執行環境需求](requirements.txt)



---


待編輯

---
直接下載即可在 jupyter notebook 或 jupyter lab 執行
套件：
1. scipy
2. statsmodels
3. os
4. datetime
5. pandas
6. numpy
有這些基本款應該就可以跑了

* TW150/TWII csv檔 可以換成你喜歡的，但不能有缺漏值、兩個的日期要統一



---

## Backtest 參數解釋

#### 1. 初始設置
```python
Backtest(strategy = 'alpha',
         beginning_money = 100, 
         start_day = '2006-01-01', 
         feature_period = 240, 
         selected_from_last = False,
         n_stock = 5, 
         max_percentage = 0.2, 
         rebalance = 240, 
         dynamic_rebalance = False, 
         stop_loss = 0.3)
```

**strategy** = ['alpha', 'beta', 'skew1', 'skew2']
* alpha: CAPM 模型之截距項
* beta: CAPM 模型之斜率項
* skew1: 每日報酬率計算的偏態
* skew2: 每年報酬率計算的偏態
> 註：策略因子可於 [套件模組](module/calculate.py) 自行調整


**beginning_money** 預設起始金額 100 元

**start_day** 預設為 '2006-01-01'

需設定在 2006 年之後  

**feature_period** 預設為 240

參數取自多長的時間，最多 240
(建議不少於 60 天)

**selected_from_last** = [True, False] 預設為 False
* True 選取參數最小者
* False 選取參數最大者

**n_stock** 預設為 5
投資組合有幾檔股票
(建議以 3 5 8 10 為主)

**max_percentage** 預設為 0.2
每一檔股票的最大權重
最小為 1 / n_stock
最大為 1

**rebalance** 預設 240
多少天靜態再平衡
（若設定 10000，將不會有靜態平衡的條件）

**dynamic_rebalance** = [True, False] 預設為 False

是否做停損再平衡

**stop_loss** 預設為 0.3

若 dynamic_rebalance = True，才會執行此條件




#### 2. 量化績效指標
```python
self.show_index(index = 'Sharpe_ratio')
```

Index 可填入以下八種指標，或呈現全部
1. Max_drawdown
2. Accumulation_return
3. Annual_return
4. Annual_volatility
5. Neg_annual_volatility
6. Sharpe_ratio
7. Sortino_ratio
8. Calmar_ratio
9. All


#### 3. 績效與回撤圖

```python
self.show_portfolio()
```

#### 4. 資產收益細節

```python
self.portfolio_benchmark
```


---

## 未來
歡迎與我合作

本次專案發現到，停損不一定 因為
#### 找出「不同投資環境」下，「獲利能力最好的因子」
1. 利用機器學習分群、或主觀判斷（波動小盤整、波動大盤整、上升型態、下跌形態）
2. 找出每一個情境下，最會賺錢的因子









