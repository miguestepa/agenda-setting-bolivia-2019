import pandas as pd
import numpy as np
import csv
import re
from collections import Counter

emotion_dict = pd.read_csv('lexicon_spanish_fixed.csv', encoding='utf-8')
tweets_bolivia = pd.read_csv('df_tweets_jaenine-añez_spanish.csv', sep = ',', encoding = "utf-8")

df_emotion = pd.DataFrame(emotion_dict)
df_tweets = pd.DataFrame(tweets_bolivia)

#print (df_emotion.emotion.unique())
df_emotion = df_emotion.drop(columns=['Unnamed: 0', 'index'])
#df_emotion.head(10)

#df_tweets
df_tweets = df_tweets.drop(columns=['has_media', 'img_urls','is_replied', 'is_reply_to', 'parent_tweet_id','reply_to_users','video_url'])

texts = pd.Series(df_tweets['text']) 
#texts.head(10) 
#print(articles[2])

list_words=[]

for text in texts:
    #print(text)
    result = text.split()
    #print(result)
    result = [x.strip("(.)") for x in result]
    result = [x.strip(",") for x in result]
    result.append([re.findall('[A-Z][^A-Z]*',i) for i in result if i.startswith('#')])
    #print(result)
    result = [i for i in result if type(i) != list]
    result = [i for i in result if not i.startswith(('#','@', 'http','+'))]
    #print(result)
    result = [i.casefold() for i in result if len(i)>3] 
    result = [i for i in result if i.isalnum() == True]
    #print(result)
    #print(result)
    result = [x.strip("(.)") for x in result]
    #print(result)
    list_words.append(result)

#print(list_words[2])

emotions_dictionary = dict(zip(df_emotion['Spanish-es'], df_emotion['emotion']))

list_of_emotions_counter = []

for tweet in list_words:
    emotional_counter = Counter()
    for word in tweet:
        if word in list(emotions_dictionary.keys()):
            emotional_counter[emotions_dictionary[word]] += 1
    list_of_emotions_counter.append(emotional_counter)

#list_of_emotions_counter[6]

n_trust = []
n_fear = []
n_surprise = []
n_joy = []
n_sadness = []
n_anger = []
n_anticipation = []
n_disgust = []

correlaction_dict = {'trust':n_trust,  
                     'fear':n_fear, 
                     'surprise': n_surprise, 
                     'joy':n_joy, 
                     'sadness':n_sadness, 
                     'anger': n_anger,
                     'anticipation':n_anticipation, 
                     'disgust':n_disgust}

for tweet in list_of_emotions_counter:
    #print(tweet)
    correlator = list(tweet.keys())
    for elem in correlaction_dict: 
        if elem in correlator:
            correlaction_dict[elem].append(tweet[elem])
        elif elem not in correlator:
            correlaction_dict[elem].append(0)
        
#     print(n_trust, n_fear, n_surprise, n_joy, n_sadness, n_anger, n_anticipation, n_disgust)    
#     print('-----------------------------')    

df_emotion_levels = pd.DataFrame(list(zip(n_trust, n_fear, n_surprise, n_joy, n_sadness, n_anger, n_anticipation, n_disgust)), 
               columns =['n_trust', 'n_fear', 'n_surprise', 'n_joy', 'n_sadness', 'n_anger', 'n_anticipation', 'n_disgust'])

df_complete = pd.concat([df_tweets, df_emotion_levels], axis=1)

df_complete.to_csv('df_tweets_jaenine-añez_emotions_spanish.csv')  
#df_complete