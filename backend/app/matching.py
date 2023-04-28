
from sqlalchemy.orm import Session

from . import schemas, models

import pandas as pd
import numpy as np
import matplotlib as mpl
import sqlite3 as sql
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier

#Data retrieval
dbConnection = sql.connect('app.db')
db = dbConnection.cursor()

results = db.execute('''
    SELECT sample.user_id, sample.keytimes
    FROM sample
''').fetchall()

user_current = db.execute('''
    SELECT user._id, user.username
    FROM user
''').fetchall()

#Data formatting
userDataRaw = {}

for userid, user in user_current:
    if userid not in userDataRaw:
        userDataRaw[userid] = []
    userDataRaw[userid].append([float(time) for time in user.strip('[]').split(',')])

#data as a dictionary of user:userid
userData = {
    user: userid
    for (userid, user) in userDataRaw.items()
}

#Data formatting
dataRaw = {}

for user, sample in results:
    if user not in dataRaw:
        dataRaw[user] = []
    dataRaw[user].append([float(time) for time in sample.strip('[]').split(',')])

#data as a dictionary of user:array(sample_array)
data = {
    i: np.array(samples)
    for i, (user, samples) in zip(range(len(dataRaw)), dataRaw.items())
    if len(samples) > 3 and user != 10
}

users = {
    user
    for user, samples in data.items()
}

sample_labels = [] 
sample_list = []
label_list = []
for label, samples in data.items():
    for sample in samples:
        sample = np.diff(sample)
        sample_labels.append((label, sample))
        sample_list.append(sample)
        label_list.append(label)

df = pd.DataFrame(sample_labels, columns=['userid','samples'])

def explode_array_column(row):
    return pd.Series(row['samples'])

expanded_cols = df.apply(explode_array_column, axis=1)
expanded_cols.columns = ['key_{}'.format(i) for i in range(expanded_cols.shape[1])]

df = pd.concat([df, expanded_cols], axis=1)
df = df.drop('samples', axis=1)

#Pre-processing for stats analysis
sc = StandardScaler()
df.loc[:, df.columns != 'userid'] = sc.fit_transform(df.loc[:, df.columns != 'userid'])

train_set, test_set = train_test_split(df, test_size=0.25, stratify=label_list)

train_x = train_set.loc[:, train_set.columns != 'userid']
train_y = train_set.loc[:, train_set.columns == 'userid']
test_x = test_set.loc[:, test_set.columns != 'userid']
test_y = test_set.loc[:, test_set.columns == 'userid']

#MLPClassifier initalization
MLPclf = MLPClassifier(hidden_layer_sizes=(150,100,50), max_iter=300, random_state=1)
MLPclf.fit(train_x, train_y.values.ravel())



def get_match(keytimes, user):
    if MLPclf.predict(keytimes) != userData[user]:
        return False
    else:
	    return True



