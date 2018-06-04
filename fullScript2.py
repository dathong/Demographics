import pandas as pd
import numpy as np
import os
from sklearn.model_selection import KFold
from sklearn import cross_validation
import sys

#df = pd.read_csv("Fold.csv",header=None)

kf = KFold(n_splits=10)

fold = 1
#expFol = "1d_nouns"
#time = "1day"
#datType = "nouns"
expFol = sys.argv[1]
time = sys.argv[2]
datType = sys.argv[3]

df = pd.read_csv("fold_" + str(datType) + ".csv",header=None)
time_window = int(time)

for train_index, test_index in kf.split([i+1 for i in range(0,10)]):
	print("TRAIN:", train_index, "TEST:", test_index)
	train_users = []
	test_users = []
	for e in train_index:
		train_users.extend(df[e])
	for e in test_index:
		test_users.extend(df[e])
	print(len(train_users),train_users[:5])
	print(len(test_users),test_users[:5])
	dts = expFol + "/fold" + str(fold)
	if not os.path.exists(dts):
		os.makedirs(dts)
	print("fold = ",fold)
	np.savetxt(dts + "/train",train_users,newline="\n",fmt='%s')
	np.savetxt(dts + "/test",test_users,newline="\n",fmt='%s')
	fold+=1

import os

df2 = pd.read_csv("tweets_data_processed_1day_" + datType + ".csv",sep="|")
df2 = df2[df2['time_stamp'] >= '2016-01-01']
# for f in [1]:
for f in range(10):
	fold = expFol + "/fold" + str(f + 1) + "/"
	train_users = pd.read_csv(fold + "train",encoding="ascii",header=None).values.flatten()
	test_users = pd.read_csv(fold + "test",encoding="ascii",header=None).values.flatten()
	df2train = df2[df2['handle'].isin(train_users)]
	df2test = df2[df2['handle'].isin(test_users)]
	print("train_users shape = ",df2train.shape,train_users.shape)
	print("test_users shape = ",df2test.shape,test_users.shape)
	dates = df2['time_stamp'].unique()
	print("dates shape = ",dates,dates.shape)
	dates = np.sort(dates)
	# for date in dates[-5:]:
	for date in dates:
		dts = fold + str(date) + "/"
		if not os.path.exists(dts):
			os.makedirs(dts)
		date_index = np.where(dates == date)[0]
		if date_index >= len(dates) - time_window - 1:
			date_indices = np.arange(date_index - time_window,len(dates))
		else:
			date_indices = np.arange(date_index - time_window,date_index + time_window + 1)
		train_dates = dates[date_indices]
		dfTrainX = df2train[df2train['time_stamp'].isin(train_dates)]
		dfTestX = df2test[df2test['time_stamp'] == date]
		dfTrainX.to_csv(dts + "train_tweets_full_" + time + "_" + datType ,index=None)
		dfTestX.to_csv(dts + "test_tweets_full_" + time + "_" + datType,index=None)
		df2trainX = dfTrainX[['hash_tags','location']]
		df2testX = dfTestX[['hash_tags','location']]
		if datType == "nouns":
			df2trainX = dfTrainX[['nouns','location']]
			df2testX = dfTestX[['nouns','location']]
		df2testUser = dfTestX[['handle']]
		df2trainX.to_csv(dts + "train_tweets_" + time + "_" + datType,header=None,index=None)
		print("dates & shape = ",date,df2testX.shape)
		df2testX.to_csv(dts + "test_tweets_" + time + "_" + datType,header=None,index=None)
