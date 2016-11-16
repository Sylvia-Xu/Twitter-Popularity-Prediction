
# coding: utf-8

# In[152]:

from sklearn import metrics
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction import text
from sklearn.decomposition import TruncatedSVD
from sklearn.linear_model import LogisticRegression
from sklearn.cross_validation import KFold
from sklearn.cross_validation import train_test_split
import numpy as np
import random
import os.path
import json
import re


# In[153]:

folder = "tweet_data"
filenames = ["tweets_#gohawks.txt", "tweets_#gopatriots.txt"]

def streamText(tagID):
    samples = []
    filename = os.path.join(folder, filenames[tagID])
    with open(filename, 'r') as textIn:
        for line in textIn:
            p = random.random()
            if p > 0.143:
                continue
            parsed = json.loads(line)
            tweet = parsed[u'highlight'].lower()
            if (tagID == 0):
                removed = re.split('#gohawks|http://t.co/[a-zA-z0-9]+', tweet)
            else:
                removed = re.split('#gopatriots|http://t.co/[a-zA-z0-9]+', tweet)
            raw = ''
            for part in removed:
                if re.match('^ *$', part) != None:
                    continue
                raw += part
            samples.append(raw)
#     print samples
    return samples


# In[154]:



X1 = streamText(tagID = 0)

y = list()
for i in range(len(X1)):
    y.append(0)
X2 = streamText(tagID = 1)
for i in range(len(X2)):
    y.append(1)
X = X1 + X2
X = np.array(X)
y = np.array(y)

        


# In[155]:

from sklearn.pipeline import Pipeline
text_clf = Pipeline([('vect', CountVectorizer()),
                     ('tfidf', TfidfTransformer()),
                     ('svd', TruncatedSVD(n_components=100)),
                     ('clf', LogisticRegression()),
])


# In[156]:




# In[159]:


accuracy = 0.0


kf = KFold(len(X), n_folds = 10)

for train, test in kf:
    trainFea = X[train]
    trainTar = y[train]
    testFea = X[test]
    testTar = y[test]
    text_clf = text_clf.fit(trainFea, trainTar)
    pred = text_clf.predict(testFea)
    accuracy += metrics.accuracy_score(testTar, pred)    
    precisions += metrics.precision_score(testTar, pred)
    recalls += metrics.recall_score(testTar, pred)
print accuracy / 10


# In[158]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:



