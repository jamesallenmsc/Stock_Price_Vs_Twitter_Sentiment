""" Main module set containing all Twitter commands
"""

import tweepy
import pandas as pd
import datetime
import time
import numpy as np

from textblob import TextBlob

__author__ = "James Allen"
__date__ = "2022-06-28"
__maintainer__ = "James Allen"
__website__ = "MeetJamesAllen.com"
__email__ = "jamesallenmsc@protonmail.com"

## Gain access to Twitter Developer account 
keys = pd.read_csv('MSc_Project_Code/Data/Twitter_Keys.csv', index_col=False, header=None)
API_Key = keys.iloc[0,1]
API_Key_Secret = keys.iloc[1,1]
Bearer_Token = keys.iloc[2,1]
Access_Token = keys.iloc[3,1]
Access_Token_Secret = keys.iloc[4,1]

client = tweepy.Client(Bearer_Token, wait_on_rate_limit = True)  # wait_on_wait_limit pauses if Twitter limit reached


def retrieve_days_tweet(search_term, from_date, to_date):
    """Retrieves 500 tweets from a given day
    """
    tweet_list = []
    tweets = client.search_all_tweets(query = search_term,start_time = from_date,end_time = to_date,max_results = 500) 
    for tweet in tweets.data:
        tweet_list.append(tweet.text)
    tweet_list_final = pd.DataFrame(tweet_list)
    print(tweet_list_final)
    return tweet_list_final


def get_sentiment(tweet_list):
    """ Generates daily sentiment polarity for Tweets
    """
    sentiment_list = pd.Series(dtype=float)
    for pos in range(len(tweet_list)):
        tweet = TextBlob(str(tweet_list.iloc[pos]))
        tweet_sentiment = pd.Series(tweet.polarity)
        sentiment_list = pd.concat([sentiment_list, tweet_sentiment])
    return sentiment_list.mean()

def count_tweets(search_term, from_date, to_date):
    """ Returns total Tweet volume for a given search term
    """
    return client.get_all_tweets_count(query = search_term,
                                        start_time=from_date,
                                        end_time=to_date,
                                        granularity='day')

# Builds data set containing tweet sentiment and volume for all days in date range
# Adds data to stock price list with close data
data_with_tweets = pd.DataFrame() 
start_date = datetime.date.fromisoformat('2014-12-26')
end_date = datetime.date.fromisoformat('2020-12-31')
increment = datetime.timedelta(days=1)
cursor_date = start_date
stocks_terms = [['$MSFT OR MSFT', 'MSFT'],
                ['$META OR META', 'META'],
                ['$GOOG OR GOOG','GOOG'],
                ['$AMZN OR AMZN', 'AMZN'], 
                ['$NFLX OR NFLX', 'NFLX']]

stock_list = pd.read_csv('MSc_Project_Code/Utilities/Data_Prep/Outputs/final_stock_data.csv')

final_stock_list = pd.DataFrame()

# Iterates over all dates
while cursor_date <= end_date:

    cursor_date_fmt = cursor_date.strftime('%Y-%m-%dT00:00:00Z')
    to_date = cursor_date + increment
    to_date_fmt = to_date.strftime('%Y-%m-%dT00:00:00Z')
    # For given date, iterate over each Twitter search term 
    for term in stocks_terms:

        search_term = f"({term[0]}) -is:retweet lang:en (Buy OR Sell)"

        check_date = cursor_date.strftime('%Y-%m-%d')
        stock_row = stock_list.loc[(stock_list['Date'] == check_date) & (stock_list['Ticker'] == term[1])]
        # Fills in weekend / bank holiday stock data using Fridays close prices
        if stock_row.empty:
            previous_day = cursor_date - increment
            previous_day = previous_day.strftime('%Y-%m-%d')
            weekend_row = pd.DataFrame(final_stock_list.loc[(final_stock_list['Date'] == previous_day) & (final_stock_list['Ticker'] == term[1])])
            weekend_row['Date'] = check_date
            
            tweet_count = count_tweets(search_term, cursor_date_fmt, to_date_fmt)
            count = tweet_count.data[0]['tweet_count']
            weekend_row['Tweet Volume'] = count
            time.sleep(1)

            try:
                tweets = retrieve_days_tweet(search_term, cursor_date_fmt, to_date_fmt)
                twitter_sentiment = get_sentiment(tweets)
                weekend_row['Sentiment'] = twitter_sentiment
                final_stock_list = pd.concat([final_stock_list, weekend_row])
            except:
                weekend_row['Sentiment'] = 0
                final_stock_list = pd.concat([final_stock_list, weekend_row])

        else:
            stock_row = pd.DataFrame(stock_row)
            tweet_count = count_tweets(search_term, cursor_date_fmt, to_date_fmt)
            count = tweet_count.data[0]['tweet_count']
            stock_row['Tweet Volume'] = count
            time.sleep(1)
            try:
                tweets = retrieve_days_tweet(search_term, cursor_date_fmt, to_date_fmt)
                twitter_sentiment = get_sentiment(tweets) 
                stock_row['Sentiment'] = twitter_sentiment
                final_stock_list = pd.concat([final_stock_list, stock_row])
            except:
                stock_row['Sentiment'] = 0
                final_stock_list = pd.concat([final_stock_list, stock_row])
                

        time.sleep(1)
        final_stock_list.to_csv('MSc_Project_Code/Utilities/Twitter_Scrape/Ouputs/Final_Output_Revised.csv', index=False)
        final_stock_list = pd.read_csv('MSc_Project_Code/Utilities/Twitter_Scrape/Ouputs/Final_Output_Revised.csv')
        final_stock_list['Date'] = final_stock_list['Date'].astype(str)
    
    cursor_date = cursor_date + increment