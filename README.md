# 單因子策略 理財機器人回測

## 專案簡介
將 2004 ~ 2020 年台灣市值前 150 大的股票（刪除早期未上市，共 108 檔）與台灣加權股價指數之 **調整後收盤價** 做一個簡易的回測系統，模擬 2006 ~ 2020 年真實交易歷程，實證機器人理財的可行性。

#### 理財機器人架構：
1. 單因子選股－CAMP 模型的 alpha, beta 指標；資產報酬率的偏態係數
2. 投資組合最佳化－Markowitz 均異最適化模型
3. 定期再平衡
4. 停損再平衡

#### 範例績效
![example1](picture_README_example/example1.png)

## 使用方法
下載此 repository，安裝相關套件後可直接於 jupyter notebook 執行 [主程式](main.ipynb)。

* [執行環境需求](requirements.txt)

> 註：可以自行更換 [股票資料](dataset/TW150_CloseAdj.csv) 與 [大盤股價](dataset/TWII_CloseAdj.csv)，需注意：(1)兩者的日期要統一 (2)事先移除缺漏值 (3)檔案格式和內建檔案相同。若有其他需求可以於 [套件模組](module/data.py) 中自行調整。


## Backtest 使用說明

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

**(1) strategy** = ['alpha', 'beta', 'skew1', 'skew2']

`使用哪一個因子作為選股方法（Required）`

* alpha: CAPM 模型之截距項
* beta: CAPM 模型之斜率項
* skew1: 每日報酬率計算的偏態
* skew2: 每年報酬率計算的偏態

> 註：策略因子可於 [套件模組](module/calculate.py) 自行調整

**(2) beginning_money**

`起始金額為多少錢（預設為 100）`

**(3) start_day**

`從哪一天開始交易（預設為 2006/1/1）`

> 註：需設定在 2006 年之後  

**(4) feature_period** 

`策略因子取自多長的時間製作（預設為 240）`

> 註：最多 240，建議不少於 60

**(5) selected_from_last** = [True, False]

`選取該因子最大或最小作為選股標準（預設為 False）`

* True 選取因子最小者
* False 選取因子最大者

**(6) n_stock**

`每次將幾檔股票放入投資組合（預設為 5）`

> 註：建議以 3 5 8 10 為主

**(7) max_percentage** 

`每一檔股票的最大配置比重（預設為 0.2）`

> 註：最小必須為 1 / n_stock；最大為 1

**(8) rebalance** 

`幾個交易日做一次靜態再平衡（預設 240）`

> 註：若設定 10000，將不會有靜態平衡的條件

**(9) dynamic_rebalance** = [True, False] 

`是否做停損再平衡（預設為 False）`

**(10) stop_loss** 

`設置停損百分比（預設為 0.3）`

> 註：當 dynamic_rebalance = True，才會執行此條件


#### 2. 量化績效指標
```python
self.show_index(index = 'Sharpe_ratio')
```

index 可填入以下八種指標，或呈現全部
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
![example2](picture_README_example/example2.png)


#### 4. 資產收益細節

```python
self.portfolio_benchmark
```
![example3](picture_README_example/example3.png)

---

## 未來
歡迎與我合作

本次專案發現到，停損不一定 因為
#### 找出「不同投資環境」下，「獲利能力最好的因子」
1. 利用機器學習分群、或主觀判斷（波動小盤整、波動大盤整、上升型態、下跌形態）
2. 找出每一個情境下，最會賺錢的因子









