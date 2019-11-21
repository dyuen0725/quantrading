import pandas as pd
import numpy as np
import nltk.sentiment.vader
import re

# Functions for cleaning Tweets

def remove_pattern(input_txt, pattern):
    #a function for removing pattern in text  
    
    r = re.findall(pattern, input_txt)
    for i in r:
        input_txt = re.sub(i, '', input_txt)        
    return input_txt

def clean_tweets(lst):
    #a function to remove noise in tweets  
    
    # remove twitter Return handles (RT @xxx:)
    lst = np.vectorize(remove_pattern)(lst, "RT @[\w]*:")
    # remove twitter handles (@xxx)
    lst = np.vectorize(remove_pattern)(lst, "@[\w]*")
    # remove URL links (httpxxx)
    lst = np.vectorize(remove_pattern)(lst, "https?://[A-Za-z0-9./]*")
    return lst

# Read the tweets from the CSV file.
df = pd.read_csv('All_tweets_replies_excluded.csv')

# Convert to datetime64 and convert UTC time used by Twitter to
# Eastern Time (New York).
df['created_at'] = pd.to_datetime(df.created_at) - np.timedelta64(5, 'h')
df['created_on'] = df.created_at.dt.date
df['created_at'] = df.created_at.dt.time

# Fix encoding of text
df = df.dropna()
df['text'] = df['text'].apply(lambda x: eval(x.replace('\xa0','')).decode('utf-8'))

#data cleaning in tweets
df['text'] = df['text'].apply(clean_tweets)

# Use Vader to obtain sentiment scores
sia = nltk.sentiment.vader.SentimentIntensityAnalyzer()
df['Sentiment'] = df['text'].apply(lambda x: sia.polarity_scores(x)['compound'])

# Write results to csv
df.to_csv('Sentiment.csv', index = None, header = True)