
# coding: utf-8

# In[32]:

import os
import json
import datetime, time
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
import random


# In[33]:

folder = "tweet_data"

filenames = ["sample1_period1.txt", "sample2_period2.txt", "sample3_period3.txt", "sample4_period1.txt", "sample5_period1.txt", "sample6_period2.txt", "sample7_period3.txt", "sample8_period1.txt", "sample9_period2.txt", "sample10_period3.txt"]
periods = [1, 2, 3, 1, 1, 2, 3, 1, 2, 3]
hashtags = ["#nfl", "#superbowl"]


# In[34]:

def extract_features_by_hour(sampleID):
    tweets = []
    count = 0
    
    os.chdir(r'/Users/xzy/Desktop/EE239P4')
    fo = os.path.join(filenames[sampleID])
    with open(fo) as json_data: 
        for line in json_data:
#             print count
            if count>=0:
                tweet=json.loads(line)
                tweets.append([tweet['firstpost_date'],tweet['metrics']['citations']['data'][0]['citations'],
#                                    tweet['tweet']['user']['id'],tweet['author']['followers'],
#                                    tweet['tweet']['entities']['user_mentions'],
#                                tweet['tweet']['favorite_count'],
                               tweet['metrics']['ranking_score']])
                count=count+1
            else:
                break
                
    time1 = int(time.mktime(datetime.datetime(2015,02,01, 8,00,0).timetuple()))
    time2 = int(time.mktime(datetime.datetime(2015,02,01, 20,00,0).timetuple()))
    
    tweet_firstpost_date=[tweet[0] for tweet in tweets]
    start=min(tweet_firstpost_date)
    end=max(tweet_firstpost_date)
    interval = (end-start)/3600
    
    time_window = [[0 for i in range(7)] for j in range(interval+2)]
    user_id = {}
    
    for i in range(len(tweets)):
        cur_time = tweets[i][0]
        
        index = (cur_time-start)/3600

        if cur_time<time1:
            interval1=index
            interval2=interval1
        elif cur_time<time2:
            interval2=index
            
        user_id[index] = set([])
        time_window[index][0] = time_window[index][0] + 1
        time_window[index][1] = time_window[index][1] + tweets[i][1]
#         # only when we encounter this user id for the first time, we need to add up the followers 
#         if time_window[index][2] not in user_id[index]:
#             user_id[index].add(time_window[index][2])
#             time_window[index][2] =time_window[index][2]+tweets[i][3]
#         time_window[index][3] = time_window[index][3] + len(tweets[i][4])
        time_window[index][2] = time_window[index][2] + tweets[i][2]
#         time_window[index][3] = time_window[index][3] + tweets[i][3]
        time_window[index-1][3] = time_window[index][0]

#     print len(time_window),interval1,interval2
    # print  np.array(time_window)

    y=[]
    for i in range(interval+1):
        y.append(time_window[i][3])
    x=[]
    for i in range(interval+1):
        x.append(time_window[i][0:3])

    X = np.array(x)
    Y = np.array(y)
    
    return X, Y
    


# In[39]:

def predict_sample(sampleID, X, y):
    # nfl model
    param1 = np.array([ 4.48646124, -5.61669578, -0.74019664])
    param2 = np.array([ 7.47422778, 0.93539117, -1.46563972])
#     param2 = np.array([19.78845057, -15.73112033, -4.17873243])
    param3 = np.array([ 4.66562397, 24.50479546, -0.91008661])
    
#     # patriot model
#     param1 = np.array([-2.34596581, -7.52201206, 0.80934099])
#     param2 = np.array([-1.30626551, -3.86436669, 0.53227116])
#     param3 = np.array([41.83769828, 104.0194687, -10.12876714])

#     # gopatriots model
#     param1 = np.array([2.25786525, 26.35818038, -0.44611495])
#     param2 = np.array([7.81483728, -1.61204611, -1.58136035])
#     param3 = np.array([2.65913743, 2.91657381, -0.37403715])
    
    period = periods[sampleID]
    if period== 1:
        pred = np.dot(X, param1)
    elif period==2:
        pred = np.dot(X, param2)
    elif period==3:
        pred = np.dot(X, param3)  
    print pred
    
    err = []
    for i in range(len(pred)-1):
        err.append(abs(y[i+1]-pred[i]))
    print err


# In[40]:

for i in range(10):
    print filenames[i]
    X, Y = extract_features_by_hour(sampleID=i)
    predict_sample(i, X, Y)


# In[ ]:



