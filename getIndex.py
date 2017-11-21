import pandas as pd
from pandas_datareader import data as dreader
from datetime import datetime


file_name = '/home/tamezarnold/Data/SPY.csv'
dr= dreader.DataReader('SPY',  'yahoo', datetime(1990, 1, 1), datetime(2017, 1, 1))
dr['Close'] = dr['Close'].pct_change()
columns_to_drop = ['High','Low','Volume','Open','Adj Close']
dr.drop(columns_to_drop,axis = 1, inplace = 1)
dr.columns = ['Pct Change']
dr.index = dr.index.strftime('%Y-%m-%d 00:00:00+00:00')
dr.to_csv(file_name)

