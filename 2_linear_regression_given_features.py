import os
import json
import time
import numpy as np
import statsmodels.api as sm

directory=os.getcwd()
for file in os.listdir(directory):
    if file.endswith('.txt'):
        	tweets = []
	        y=[]
	        loaded_file=open(file)
	        for line in loaded_file:
	            tweets.append(json.loads(line))
	        tweet_firstpost_date=[tweet['firstpost_date'] for tweet in tweets]
	        start_time=min(tweet_firstpost_date)
	        end_time=max(tweet_firstpost_date)
	        time_interval = (end_time-start_time)/3600
	        time1= [[0 for j in range(5)] for k in range(time_interval+2)]

	        for i in range(len(tweets)):
		        cur_time = tweets[i]['firstpost_date']
		        indice = (cur_time-start_time)/3600
		        time1[indice][0] = time1[indice][0]+1
		        time1[indice][1] = time1[indice][1]+tweets[i]['metrics']['citations']['data'][0]['citations']
		        time1[indice][2] = time1[indice][2]+tweets[i]['author']['followers']
		        time1[indice][3] = max(time1[indice][3],tweets[i]['tweet']['user']['followers_count'])
		        cur_time = time.strftime('%H:%M:%S', time.gmtime(cur_time))
		        time1[indice][4] = int(cur_time[0])*10+int(cur_time[1])

	        for k in range(time_interval+1):
		        y.append(time1[k+1][0])

	        del time1[-1]
	        X = np.array(time1)
	        Y = np.array(y)
	        model = sm.OLS(Y, X)
	        model_result = model.fit()

	        hashtag=file[7:-4]
            #create Time file
	        Time = open('Time', 'a')
	        print>>Time, hashtag
	        print>>Time, time1
	        Time.close()

	        Linear_Regression = open('Linear_Regression', 'a')
	        print(model_result.summary())

	        print>>Linear_Regression, hashtag
	        #result write in file
	        print>>Linear_Regression, model_result.summary()
	        Linear_Regression.close()


	        loaded_file.close()   

