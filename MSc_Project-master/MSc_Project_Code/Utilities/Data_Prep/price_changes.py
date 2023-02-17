import numpy as np
import pandas as pd
import datetime


# READ CSV, FILTER OUT PRE-DESIGNATED STOCKS AND ASSIGN TO 'filtered_stocks'
full_stock = pd.read_csv("MSc_Project_Code/Utilities/Data_Prep/Outputs/s&p_price_history.csv",
                        parse_dates=True)

target_stocks = ["MSFT", "META", "GOOG", "AMZN", "NFLX"]
stock_list = pd.DataFrame(full_stock[full_stock.Ticker.isin(target_stocks)])


stock_list.to_csv("MSc_Project_Code/Utilities/Data_Prep/Outputs/final_stock_data.csv",
                index=False)
stock_list = pd.read_csv("MSc_Project_Code/Utilities/Data_Prep/Outputs/final_stock_data.csv",
                        parse_dates=True)



# FUNCTION TO FIND THE PRICE CHANGE OVER A GIVEN TIMEFRAME
def abs_price_change(stock_list, ticker, start_date, period):
    """Takes a stock list as a dataframe ticker symbol, a given date,
    and a time period and returns the greatest change over that period
    """
    start = datetime.date.fromisoformat(start_date)
    increment = datetime.timedelta(days=period)
    filt = (stock_list['Date'] >= str(start))\
            & (stock_list['Date'] <= str(start + increment))\
            & (stock_list['Ticker'] == ticker)
    period = stock_list.loc[filt]
    change = period['Close'] - period.iloc[0, 2] # Subtracts initial value from column
    largest_change = 0
    for i in change:
        if abs(i) > largest_change:
            largest_change = i
    return largest_change


# RUNS PERCENTAGE PRICE CHANGE FOR GIVEN INPUTS
def find_percent_change(initial_value, change):
    percent_change = ((((initial_value + change) / initial_value) - 1)) * 100
    return percent_change


# Run 'abs_price_change' for each line in stock list
# Run 'find_percent_change' for each line in stock list
stock_list["14 Day Price Change"] = np.nan
stock_list["14 Day % Change"] = np.nan
for index, row in stock_list.iterrows():
    period = 14
    start_date = row['Date']
    ticker = row['Ticker']
    price_change = abs_price_change(stock_list,
                                    ticker,
                                    start_date,
                                    period)
    stock_list.iloc[index, 3] = round(price_change, 3)
    close_price = row['Close']
    percent_change = find_percent_change(close_price, price_change)
    stock_list.iloc[index, 4] = round(percent_change, 3)


stock_list.to_csv("MSc_Project_Code/Utilities/Data_Prep/Outputs/final_stock_data.csv",
                index=False)
