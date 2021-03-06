import tweepy
import numpy as np
import pandas as pd
import keys 
import time 
import matplotlib
import re 
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

#authentication
auth = tweepy.OAuthHandler(keys.CONSUMER_KEY, keys.CONSUMER_SECRET)
auth.set_access_token(keys.ACCESS_TOKEN, keys.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)
df = pd.DataFrame(columns=['Tweets'])

#getting search requests from user 
def askSearch() : 
    search = ''
    searches = []
    while search != 'done' : 
        search = input("Enter done when done. Enter a term to search : ")
        if search == 'done' : 
            break 
        else : 
            searches.append(search)
    return searches 

#storing tweets in datafrane 
def storeTweets(search) : 
    i = 0 
    for tweet in tweepy.Cursor(api.search, q=search, count=1000, lang="en").items() : 
        df.loc[i, 'Tweets'] = tweet.text
        i += 1 
        if i == 1000 : 
            break
        else : 
            pass 
        
#removing certain characters to make sentiment analysis easier 
def cleanTweet(tweet) : 
    return ' '.join(re.sub('(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)', ' ', tweet).split())

# use VADER to perform sentiment analysis on stored tweets
analyser = SentimentIntensityAnalyzer()

#performing sentiment analysis 
#assigning Positive, Negative or Neutral depending on the polarity score 
def sentiment_analysis(tweet):
    #using the compound vader score 
   current_sentiment = analyser.polarity_scores(tweet)["compound"]   
   if current_sentiment > 0 : 
       return 'Positive'
   if current_sentiment == 0 : 
       return 'Neutral'
   else : 
       return 'Negative'

#asking for search terms and storing them 
storeTweets(search=[askSearch()])
#cleaning tweets and adding them to a new column 
df['clean_tweet'] = df['Tweets'].apply(lambda x: cleanTweet(x))
#applying sentiment analysis and adding a new column 
df['Sentiment'] = df['clean_tweet'].apply(lambda x: sentiment_analysis(x))
#plotting a bar graph with the data found 
#counts number of positive, negative and neutral sentiments 
df['Sentiment'].value_counts().plot(kind='barh')
