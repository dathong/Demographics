import pandas as pd
import numpy as np
import os
from sklearn.model_selection import KFold
from sklearn import cross_validation
import sys

df = pd.read_csv("Fold.csv",header=None)

kf = KFold(n_splits=10)


fold = 1
#expFol = "1d_nouns"
#time = "1day"
#datType = "nouns"
expFol = sys.argv[1]
time = sys.argv[2]
datType = sys.argv[3]


df2 = pd.read_csv("tweets_data_processed_" + time + "_" + datType + ".csv",sep="|")
# for f in [1]:
for f in range(10):
	fold = expFol + "/fold" + str(f + 1) + "/"
	train_users = pd.read_csv(fold + "train",encoding="ascii",header=None).values.flatten()
	test_users = pd.read_csv(fold + "test",encoding="ascii",header=None).values.flatten()
	df2train = df2[df2['handle'].isin(train_users)]
	df2test = df2[df2['handle'].isin(test_users)]
	print("train,users shape = ",df2train.shape,train_users.shape)
	print("test,users shape = ",df2test.shape,test_users.shape)
	 	
	df2train.to_csv(fold + "train_tweets_full_" + time + "_" + datType ,index=None)
	df2test.to_csv(fold + "test_tweets_full_" + time + "_" + datType,index=None)
	df2trainX = df2train[['hashtags','location']]
	df2testX = df2test[['hashtags','location']]
	if datType == "nouns":
		df2trainX = df2train[['nouns','location']]
		df2testX = df2test[['nouns','location']]
	print("train shape & test shape = ",df2trainX.shape,df2testX.shape)
	df2trainX.to_csv(fold + "train_tweets_" + time + "_" + datType,header=None,index=None)
	df2testX.to_csv(fold + "test_tweets_" + time + "_" + datType,header=None,index=None)

	print("Done")
