"""This module takes data from Yahoo finance and ascertains which of the assets have the greatest 
weekly variance in stock price. Specifically across the S&P 500 """

from os import truncate
from requests import head
import yfinance as yf
import pandas as pd

__author__ = "James Allen"
__date__ = "2022-06-12"
__version__ = "1.0.1"
__maintainer__ = "James Allen"
__email__ = "jamesallenmsc@protonmail.com"

# Import s&p 500 data, strip whitespace from left and right of column names and
# remove spaces
sp_const_data = pd.read_csv("MSc_Project_Code/Data/SP_500_Company_List.csv", header = 0)
sp_const_data.columns = sp_const_data.columns.str.lstrip()
sp_const_data.columns = sp_const_data.columns.str.rstrip()
sp_const_data.columns = sp_const_data.columns.str.replace(' ','_')

sp_const_data['Symbol'] = sp_const_data['Symbol'].str.rstrip()
symbols = sp_const_data['Symbol']

sp_stock_list = pd.DataFrame()

for stock in symbols:
    asset_temp = yf.Ticker(stock)
    asset_hist = asset_temp.history(start="2014-12-25", end="2021-02-1")
    asset_hist = pd.DataFrame(asset_hist['Close'])
    asset_hist['Ticker'] = stock
    asset_hist = asset_hist[['Ticker', 'Close']]
    sp_stock_list = pd.concat([sp_stock_list, asset_hist])

sp_stock_list.to_csv("MSc_Project_Code/Utilities/Data_Prep/Outputs/s&p_price_history.csv")