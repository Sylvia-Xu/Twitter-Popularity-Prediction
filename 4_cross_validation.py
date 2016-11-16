
# coding: utf-8

# In[33]:

import os
import json
import datetime, time
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
import random
from sklearn.cross_validation import KFold


# In[34]:

folder = "tweet_data"

filenames = ["tweets_#gohawks.txt", "tweets_#gopatriots.txt", "tweets_#nfl.txt", "tweets_#patriots.txt", "tweets_#sb49.txt", "tweets_#superbowl.txt"]
hashtags = ["#gohawks", "#gopatriots", "#nfl", "#patriots", "#sb49", "#superbowl"]


# In[35]:

def crossValidation(tagID):
    tweets = []
    hashtag=hashtags[tagID]
    count = 0
    
    os.chdir(r'/Users/xzy/Desktop/EE239P4')
    fo = os.path.join(filenames[tagID])
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
    interval1=0
    interval2=0
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
        
    time_window_random = random.sample(time_window, len(time_window))

#     print len(time_window),interval1,interval2
    # print  np.array(time_window)

    y=[]
    for i in range(interval):
        y.append(time_window_random[i][3])
    x=[]
    for i in range(interval):
        x.append(time_window_random[i][0:3])

    X = np.array(x)
    Y = np.array(y)
    
    def FitAndValidate(X,y,period):
        cross_err = []
        cross_err1 = []
        cross_avg = []
        print "period: "+str(period)
        
        kf = KFold(X.shape[0],n_folds=10)
        for train, test in kf:
            
#             X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.1, random_state=0)
#             print(target.shape[0])
#             print(train.shape[0])
            model = sm.OLS(y[train], X[train])
            results = model.fit()
#             print "model params: ",results.params
#             print results.summary()
            
            pred_err1=0
            for i in range(len(y[train])):
                pred_err1 += abs(y[train][i]-sum(results.params*X[train][i]))
            cross_err1.append(pred_err1/len(y[train]))
            
            pred_err=0
            y_test = y[test]
            X_test = X[test]
            for i in range(len(y[test])):
                pred_err +=  abs(y_test[i]-sum(results.params*X_test[i]))
#                 print y[test][i]
#                 print sum(results.params*X[test][i])
            cross_err.append(pred_err/len(y_test))
            cross_avg.append(np.mean(y_test))
        avg_err=np.mean(cross_err)
        avg_err1=np.mean(cross_err1)

#         f = open("cross_validation_err_"+hashtag+".txt",'a')
#         print>>f,"cross_error of period "+str(period)+" :"
#         print>>f, cross_err
#         print>>f,"cross_avg of period "+str(period)+" :"
#         print>>f, cross_avg
#         print>>f,"cross_error_avg of period "+str(period)+" :"
#         print>>f, avg_err
#         # print>>f,"model params:"
#         # print>>f,results.params
#         print>>f,""
#         f.close()
#         print cross_err
#         print cross_avg
        print avg_err1
        print avg_err
    
    
    X1 = X[0:interval1+1]
    Y1 = Y[0:interval1+1]
#     print(X1.shape[0])
#     print(Y1.shape[0])
    FitAndValidate(X1,Y1,0)

    X2 = X[interval1+1:interval2+1]
    Y2 = Y[interval1+1:interval2+1]

    FitAndValidate(X2,Y2,1)

    X3 = X[interval2:]
    Y3 = Y[interval2:]
    FitAndValidate(X3,Y3,2)


# In[36]:

# for i in range(6):
#     crossValidation(tagID=i)

crossValidation(tagID=1)
    


# In[ ]:



