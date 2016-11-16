
# coding: utf-8

# In[8]:

import os
import json
import pprint
import datetime
from sets import Set
from datetime import timedelta
import os.path
import statsmodels.api as sm
from sklearn import linear_model
from sklearn.metrics import accuracy_score
from sklearn.metrics import mean_squared_error
from sklearn.feature_selection import f_regression

from matplotlib import pyplot as plt
get_ipython().magic(u'matplotlib inline')

folder = "tweet_data"
filenames = ["tweets_#gohawks.txt", "tweets_#gopatriots.txt", "tweets_#nfl.txt", "tweets_#patriots.txt", "tweets_#sb49.txt", "tweets_#superbowl.txt"]

def load_features_by_hour(tagID):
    features_dict = {}
    fo = filenames[tagID] + ".json"

    if not os.path.exists(fo):
        print "file does not exist yet, creating it now..."
#         extract_features_by_hour(tagID)

    with open(fo, 'rb') as json_data:
        for json_item in json_data:
            features_dict = json.loads(json_item)
    

    d = {}
    for key in features_dict:
        cur_hour = datetime.datetime.strptime(key, "%Y-%m-%d %H:%M:%S")
        value = features_dict[key]
        d[cur_hour] = value
#         print d
    return d

def construct_matrix(d):
    """ 
        Construct X, y for regression 
        here y is the number of tweets for next hour
    """
    start_time = min(d.keys()) 
    end_time = max(d.keys())
    X = []
    y = []
    cur_hour = start_time
    while cur_hour < end_time:

        """ y value """
        tweets_count_next_hour = 0
        next_hour = cur_hour+timedelta(hours=1)
        if next_hour in d:
            tweets_count_next_hour = d[next_hour]['tweets_count']

        """ X values """
        if cur_hour in d:
            #item = d[cur_hour].values() + [tweets_count_next_hour]
            X.append(d[cur_hour].values())
            y.append([tweets_count_next_hour])
            #print item
        else:
            temp = {'tweets_count':0, 'retweets_count':0, 'followers_count':0, 'max_followers':0, 'author_count':0, 'mention_count':0, 'ranking':0, 'time':cur_hour.hour}
            #item = temp.values() + [tweets_count_next_hour]
            X.append(temp.values())
            y.append([tweets_count_next_hour])
            #print item

        cur_hour = next_hour

    return X, y


 
if __name__ == "__main__":

    for i in range(6):
        d = load_features_by_hour(tagID = i)
        X, y = construct_matrix(d)

        lr = linear_model.LinearRegression()
        lr.fit(X,y)
    
        y_pred = lr.predict(X)

        model = sm.OLS(y, X)
        results = model.fit()
        print(results.summary())
        X_1 = list()
        X_2 = list()
        X_4 = list()
        for i in range(0, len(X)):
            X_1.append(X[i][0])
            X_2.append(X[i][1])
            X_4.append(X[i][3])
       
        plt.figure(1)
        plt.xlabel('tweets_count')
        plt.ylabel('Predictant-number of tweets for next hour')
        plt.title('Predictant versus tweets_count')
        plt.scatter(X_1, y_pred, alpha=0.5)

        plt.figure(2)
        plt.xlabel('retweets_count')
        plt.ylabel('Predictant-number of tweets for next hour')
        plt.title('Predictant versus retweets_count')
        plt.scatter(X_2, y_pred, alpha=0.5)

        plt.figure(3)
        plt.xlabel('max_followers')
        plt.ylabel('Predictant-number of tweets for next hour')
        plt.title('Predictant versus max_followers')
        plt.scatter(X_4, y_pred, alpha=0.5)

        plt.show()
        
    
        


# In[9]:

# print X[0][7]
X_6 = list()
X_5 = list()
X_3 = list()
for i in range(0, len(X)):
    X_6.append(X[i][6])
    X_5.append(X[i][5])
    X_3.append(X[i][3])


# In[ ]:



