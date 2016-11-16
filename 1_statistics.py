
# coding: utf-8

# In[13]:

import os
import json
import datetime
import os.path


# In[14]:

from datetime import timedelta
# from extract_features import extract_features_with_hour_window
import matplotlib.pyplot as plt


# In[15]:

folder = "tweet_data"
# filenames = ["tweets_#nfl.txt", "tweets_#superbowl.txt"]
# hashtags = ["#nfl", "#superbowl"]

filenames = ["tweets_#gohawks.txt", "tweets_#gopatriots.txt", "tweets_#nfl.txt", "tweets_#patriots.txt", "tweets_#sb49.txt", "tweets_#superbowl.txt"]
hashtags = ["#gohawks", "#gopatriots", "#nfl", "#patriots", "#sb49", "#superbowl"]


# In[16]:

def extract_features_with_hour_window(tag):
    # fo = filenames[tag] + ".json"
    #
    # if not os.path.exists(fo):
    #     print ("file does not exist yet, creating it now...")

    followers_num = 0
    retweets_num = 0
    tweets_num = 0
    total_hours = 0
    user_id_list = set([])

    start_date = datetime.datetime(2016, 3, 9)
    end_date = datetime.datetime.fromtimestamp(datetime.MINYEAR)

    general_data = {}
    user_data = {}

    os.chdir(r'/Users/xzy/Documents/ee239p4')

    fo = os.path.join(filenames[tag])

    with open(fo) as json_data:
        for json_line in json_data:
            tweet = json.loads(json_line)

            # extract date
            date = tweet["firstpost_date"]
            date = datetime.datetime.fromtimestamp(date)
            if date < start_date:
                start_date = date
            elif date > end_date:
                end_date = date
            time = datetime.datetime(date.year, date.month, date.day, date.hour, 0, 0)
            time = unicode(time)

            retweets = tweet["metrics"]["citations"]["data"][0]["citations"]
            # print retweets
            user_id = tweet["tweet"]["user"]["id"]
            followers = tweet["author"]["followers"]

            # initialize a new record in the dataset
            if time not in general_data:
                general_data[time] = {'tweets_num': 0, 'retweets_num': 0, 'followers_num': 0, 'max_followers': 0, 'time': -1}
                user_data[time] = set([])

            general_data[time]['tweets_num'] += 1
            general_data[time]['retweets_num'] += retweets
            general_data[time]['time'] = date.hour
            general_data[time]['followers_num'] += followers

            if user_id not in user_data[time]:
                user_data[time].add(user_id)
                if followers > general_data[time]['max_followers']:
                    general_data[time]['max_followers'] = followers
            if user_id not in user_id_list:
                user_id_list.add(user_id)
                followers_num += followers

            tweets_num += 1
            retweets_num += retweets


    total_hours = int((end_date - start_date).total_seconds()/3600 + 0.5)
    stats_list = {'total_tweets_num':tweets_num, 'total_hours': total_hours,
                  'total_user_num':len(user_id_list), 'total_retweets_num': retweets_num,
                  'total_followers_num': followers_num}

    avg_tweets = int(tweets_num/total_hours)
    avg_followers = int(followers_num/len(user_id_list))
    avg_retweets = int(retweets_num/total_hours)
    print avg_tweets
    print avg_followers
    print avg_retweets
    
    with open(filenames[tag]+'.json', 'wb') as fp:
        json.dump(general_data, fp)

    with open(filenames[tag]+'stats.json', 'wb') as fp:
        json.dump(stats_list, fp)


        # extract_features_by_hour(tag)
    features_dict = {}

    fo = filenames[tag] + ".json"
    with open(fo, 'rb') as json_data:
        for json_item in json_data:
            features_dict = json.loads(json_item)

    d = {}
    for key in features_dict:
        cur_hour = datetime.datetime.strptime(key, "%Y-%m-%d %H:%M:%S")
        value = features_dict[key]
        d[cur_hour] = value
        #print cur_hour, value
    return d


# In[17]:

def plot_histogram(tag, d):
    sorted_d = d
    start_time = min(sorted_d.keys())
    end_time = max(sorted_d.keys())

    tweets_per_hour = []

    cur = start_time
    while cur <= end_time:
        if cur in sorted_d:
            tweets_per_hour.append(sorted_d[cur]["tweets_num"])
        else:
            tweets_per_hour.append(0)

        cur += timedelta(hours=1)

    plt.figure(figsize=(20, 8))
    plt.title("Number of Tweets in Hour for [" + hashtags[tag] + "]")
    plt.ylabel("number of tweets")
    plt.xlabel("timeline")
    plt.bar(range(len(tweets_per_hour)), tweets_per_hour, width=1.5, color='b')
    plt.show()


# In[18]:

if __name__ == "__main__":
    
    for i in range(6):
        print hashtags[i]
        d = extract_features_with_hour_window(tag=i)
        # nfl
        if i == 2:
            plot_histogram(i, d)
        # superbowl
        if i == 5:
            plot_histogram(i, d)          
        


# In[ ]:



