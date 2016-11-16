
# coding: utf-8

# In[2]:

import os
import json
import pprint
import datetime
from sets import Set
from datetime import timedelta
import os.path


import statsmodels.api as sm
from statsmodels.sandbox.regression.predstd import wls_prediction_std


folder = "tweet_data"
filenames = ["tweets_#gohawks.txt", "tweets_#gopatriots.txt", "tweets_#nfl.txt", "tweets_#patriots.txt", "tweets_#sb49.txt", "tweets_#superbowl.txt"]

def extract_features_by_hour(tagID):

    """ construct a hashmap to store the timestamp """
    d = {}
    user_dicts = {}
    """ read necessary data from file """
    fo = os.path.join(folder, filenames[tagID])

    with open(fo) as json_data:
        for json_line in json_data:

            tweet = json.loads(json_line)
            retweets = tweet["metrics"]["citations"]["data"][0]["citations"]
            user_id = tweet["tweet"]["user"]["id"]
            followers = tweet["author"]["followers"]
            mention = len(tweet['tweet']['entities']['user_mentions'])
            ranking_score=tweet['metrics']['ranking_score']

            date = tweet["firstpost_date"]
            date = datetime.datetime.fromtimestamp(date)
            time_key = datetime.datetime(date.year, date.month, date.day, date.hour, 0, 0)
            time_key = unicode(time_key)

            if time_key not in d:
                d[time_key] = {'tweets_count':0, 'retweets_count':0, 'followers_count':0, 'max_followers':0, 'author_count':0, 'mention_count':0, 'ranking':0, 'time':-1}
                user_dicts[time_key] = Set([])
              
        
            d[time_key]['tweets_count'] += 1
            d[time_key]['retweets_count'] += retweets
            if user_id not in user_dicts[time_key]:
                user_dicts[time_key].add(user_id)
                d[time_key]['followers_count'] += followers
                if followers > d[time_key]['max_followers']:
                    d[time_key]['max_followers'] = followers
            d[time_key]['time'] = date.hour
            d[time_key]['author_count'] = len(user_dicts)
            d[time_key]['mention_count'] += mention
            d[time_key]['ranking'] += ranking_score

   
    for key in d:
        print key, 'values', d[key]

    with open(filenames[tagID]+'.json', 'wb') as fp:
        json.dump(d, fp)


if __name__ == "__main__":

    for i in range(6):
        extract_features_by_hour(tagID = i)




# In[ ]:




# In[ ]:



