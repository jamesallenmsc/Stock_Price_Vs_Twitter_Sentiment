import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import Normalizer
import datetime


data_load = pd.read_csv('Visualisations/Final_Output_Revised.csv')

def normalise_stock(data_load, ticker):
    """Takes a ticker symbol and data set and returns normalised data frame
    """
    data_mask = data_load['Ticker'] == ticker
    data_filtered = pd.DataFrame(data_load[data_mask])
    data_handle = data_filtered.iloc[:, 2:7]
    
    data_handle = pd.DataFrame(data_handle / data_handle.max())
    data_final = pd.DataFrame(np.concatenate((data_filtered, data_handle), axis=1))
    data_final = data_final.drop(data_final.columns[2:7], axis=1)
    data_final.columns =['Date', 'Ticker', 'Close', '14 Day Price Change', '14 Day % Change', 'Tweet Volume', 'Sentiment']
    data_final['Date'] = pd.to_datetime(data_final['Date'])
    return data_final


plt.rcParams['figure.figsize'] = [20, 20]
fig, axis = plt.subplots(5, 2)
plt.style.use('ggplot')


msft = normalise_stock(data_load, 'MSFT')
print(msft)
axis[0, 0].plot(msft['Date'], msft['14 Day % Change'], linewidth=0.5, label='Price Change')
axis[0, 0].plot(msft['Date'], msft['Tweet Volume'], linewidth=0.5, label='Volume')
axis[0, 0].axvline(x= (datetime.datetime(2020, 1, 1)), color = 'red', linestyle='--')

axis[0, 0].title.set_text('Microsoft "MSFT" (Tweet Volume)')
axis[0, 0].legend()

axis[0, 1].plot(msft['Date'], msft['14 Day % Change'], linewidth=0.5, label='Price Change')
axis[0, 1].plot(msft['Date'], msft['Sentiment'], linewidth=0.5, label='Sentiment')
axis[0, 1].axvline(x= (datetime.datetime(2020, 1, 1)), color = 'red', linestyle='--')

axis[0, 1].title.set_text('Microsoft "MSFT" (Sentiment)')
axis[0, 1].legend()


nflx = normalise_stock(data_load, 'NFLX')

axis[1, 0].plot(nflx['Date'], nflx['14 Day % Change'], linewidth=0.5, label='Price Change')
axis[1, 0].plot(nflx['Date'], nflx['Tweet Volume'], linewidth=0.5, label='Volume')
axis[1, 0].axvline(x= (datetime.datetime(2020, 1, 1)), color = 'red', linestyle='--')

axis[1, 0].title.set_text('Netflix "NFLX" (Tweet Volume)')
axis[1, 0].legend()

axis[1, 1].plot(nflx['Date'], msft['14 Day % Change'], linewidth=0.5, label='Price Change')
axis[1, 1].plot(nflx['Date'], msft['Sentiment'], linewidth=0.5, label='Sentiment')
axis[1, 1].axvline(x= (datetime.datetime(2020, 1, 1)), color = 'red', linestyle='--')

axis[1, 1].title.set_text('Netflix "NFLX" (Sentiment)')
axis[1, 1].legend()


meta = normalise_stock(data_load, 'META')

axis[2, 0].plot(meta['Date'], meta['14 Day % Change'], linewidth=0.5, label='Price Change')
axis[2, 0].plot(meta['Date'], meta['Tweet Volume'], linewidth=0.5, label='Volume')
axis[2, 0].axvline(x= (datetime.datetime(2020, 1, 1)), color = 'red', linestyle='--')

axis[2, 0].title.set_text('Facebook "META" (Tweet Volume)')
axis[2, 0].legend()


axis[2, 1].plot(meta['Date'], meta['14 Day % Change'], linewidth=0.5, label='Price Change')
axis[2, 1].plot(meta['Date'], meta['Sentiment'], linewidth=0.5, label='Sentiment')
axis[2, 1].axvline(x= (datetime.datetime(2020, 1, 1)), color = 'red', linestyle='--')

axis[2, 1].title.set_text('Facebook "META" (Sentiment)')
axis[2, 1].legend()


goog = normalise_stock(data_load, 'GOOG')

axis[3, 0].plot(goog['Date'], goog['14 Day % Change'], linewidth=0.5, label='Price Change')
axis[3, 0].plot(goog['Date'], goog['Tweet Volume'], linewidth=0.5, label='Volume')
axis[3, 0].axvline(x= (datetime.datetime(2020, 1, 1)), color = 'red', linestyle='--')

axis[3, 0].title.set_text('Google "GOOG" (Tweet Volume)')
axis[3, 0].legend()

axis[3, 1].plot(goog['Date'], goog['14 Day % Change'], linewidth=0.5, label='Price Change')
axis[3, 1].plot(goog['Date'], goog['Sentiment'], linewidth=0.5, label='Sentiment')
axis[3, 1].axvline(x= (datetime.datetime(2020, 1, 1)), color = 'red', linestyle='--')

axis[3, 1].title.set_text('Google "GOOG" (Sentiment)')
axis[3, 1].legend()


amzn = normalise_stock(data_load, 'AMZN')

axis[4, 0].plot(amzn['Date'], amzn['14 Day % Change'], linewidth=0.5, label='Price Change')
axis[4, 0].plot(amzn['Date'], amzn['Tweet Volume'], linewidth=0.5, label='Volume')
axis[4, 0].axvline(x= (datetime.datetime(2020, 1, 1)), color = 'red', linestyle='--')

axis[4, 0].title.set_text('Amazon "AMZN" (Tweet Volume)')
axis[4, 0].legend()

axis[4, 1].plot(amzn['Date'], amzn['14 Day % Change'], linewidth=0.5, label='Price Change')
axis[4, 1].plot(amzn['Date'], amzn['Sentiment'], linewidth=0.5, label='Sentiment')
axis[4, 1].axvline(x= (datetime.datetime(2020, 1, 1)), color = 'red', linestyle='--')

axis[4, 1].title.set_text('Amazon "AMZN" (Sentiment)')
axis[4, 1].legend()

# plt.show()
plt.savefig('Visualisations/plot.pdf')



plt.rcParams['figure.figsize'] = [10, 10]
fig, axis = plt.subplots()
plt.style.use('ggplot')

start = datetime.datetime(2019, 1, 1)
end = datetime.datetime(2020, 12, 31)

meta = normalise_stock(data_load, 'META')
mask = (meta['Date'] >= start) & (meta['Date'] <= end)
print(mask)

meta = pd.DataFrame(meta[mask])


axis.plot(meta['Date'], meta['14 Day % Change'], linewidth=0.5, label='Price Change')
axis.plot(meta['Date'], meta['Sentiment'], linewidth=0.5, label='Sentiment')
axis.plot(meta['Date'], meta['Tweet Volume'], linewidth=0.5, label='Volume')
axis.axvline(x= (datetime.datetime(2020, 1, 1)), color = 'red', linestyle='--')

axis.title.set_text('Facebook "META"')
axis.legend()
plt.savefig('Visualisations/singleplot.pdf')