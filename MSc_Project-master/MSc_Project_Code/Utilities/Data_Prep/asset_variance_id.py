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


sp_stock_list = pd.read_csv("MSc_Project_Code/Utilities/Data_Prep/Outputs/s&p_price_history.csv", header=0)


group = sp_stock_list.groupby(['Ticker']).var()
group.rename(columns={'Close':'Variance'}, inplace=True)
group = group.round(2)
group.sort_values(by=['Variance'], inplace=True, ascending=False)

group.to_csv('MSc_Project_Code/Utilities/Data_Prep/Outputs/var_list.csv')