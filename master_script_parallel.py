import pandas as pd
import numpy as np
import json
import os
from sklearn.model_selection import KFold
from sklearn import cross_validation
import naiveBayesNPP_prior 
import naiveBayesNPP_onlyMaxWord
from merge_results_parallel import merge_results
from multiprocessing import Process
import sys

#----input params----
expFol = "test_master_script_parallel"
final_output = "final_tweets_1_test.csv"
replace_flag = True
date_cutoff = '2016-12-10'
time_window = 0 #1,2,3
data_type = "hash_tags"
#data_type = "nouns"
city_format_file = "tweetMAFormatFull"
input_csv_file = "states_data/tweetMA_Hash.csv"
row_num = 1000000
user_fold_file = "states_data/Folds/FoldMA.csv"
nb_type = "normal" #"normal" or "mw"
col_list = ['user_id','tweet_id','handle','time_stamp','full_tweet','location','coordinates','city_flag','retweet_flag','hash_tags','has_hash_tags','nouns','has_nouns']
#----
#----temp files ------
processed_csv_file = expFol + "/tweets_data_processed_" + data_type + ".csv"


#--get city list---
if not os.path.exists(processed_csv_file) or replace_flag:
	lines = open(city_format_file,"r").readlines()[0]
	city_list = lines.split("|")
	locs = city_list[6:]
	df = pd.read_csv(input_csv_file,names=col_list,index_col=False,nrows=row_num)
	print("df shape = ",df.shape)
	df['time_stamp'] = df['time_stamp'].str.split(" ").str[0].replace(" ","_")
	df = df[df['time_stamp'] >= date_cutoff]
	df = df[df.location.isin(locs)]
	df = df[~df[data_type].isnull()]
	df[data_type] = df[data_type].str.replace(","," ").str.lower()
	print("df shape filtered = ",df.shape)
	loc = {}
	locList = df['location'].values
	coorList = df['coordinates'].values

	for i,e in enumerate(locList):
		if e not in loc:
			loc[e] = coorList[i]

	import json
	with open('locations.json', 'w') as fp:
		json.dump(loc, fp)

	df.to_csv(processed_csv_file,sep="|") 

dayDf = pd.read_csv(processed_csv_file,sep="|")
np.savetxt("timestamp_" + data_type,dayDf['time_stamp'].unique() ,newline="\n",fmt='%s')
#_--begin script 2 generate folds of users----

import sys

df = pd.read_csv(user_fold_file,header=None)

kf = KFold(n_splits=10)


fold = 1
#expFol = str(time_window + 1) + "_" + data_type
#time = "1day"
#datType = "nouns"
if not os.path.exists(expFol + "/fold" + str(fold)) or replace_flag:

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

	df2 = pd.read_csv(processed_csv_file,sep="|",nrows=row_num)
	dates = df2['time_stamp'].unique()
	print("dates shape = ",dates,dates.shape)
	dates = np.sort(dates)
	for fold in range(1,11):
		for date in dates:
			dts = expFol + "/fold" + str(fold) + "/" +  str(date) + "/"
			if not os.path.exists(dts):
				os.makedirs(dts)


	def genTrainTweets(df2,expFol,f):
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
			dfTrainX.to_csv(dts + "train_tweets_full_" + str(time_window + 1) + "_" + data_type ,index=None)
			dfTestX.to_csv(dts + "test_tweets_full_" + str(time_window + 1) + "_" + data_type,index=None)
			df2trainX = dfTrainX[['hash_tags','location']]
			df2testX = dfTestX[['hash_tags','location']]
			if data_type == "nouns":
				df2trainX = dfTrainX[['nouns','location']]
				df2testX = dfTestX[['nouns','location']]
			df2testUser = dfTestX[['handle']]
			df2trainX.to_csv(dts + "train_tweets_" + str(time_window + 1) + "_" + data_type,header=None,index=None)
			print("fold, dates & shape = ",f,date,df2testX.shape)
			df2testX.to_csv(dts + "test_tweets_" + str(time_window + 1) + "_" + data_type,header=None,index=None)
	procs = []
	for f in range(10):
		proc = Process(target=genTrainTweets, args=(df2,expFol,f))
		procs.append(proc)
		proc.start()
	for proc in procs:
		proc.join()

#sys.exit()

#---run NB classifier----
fold = 2
dataList = np.genfromtxt("timestamp_" + data_type,dtype='str')
dataList = np.unique(dataList)
resultFile = expFol + "/fold" + str(fold) + "/" + dataList[1] + "/result_" + str(time_window + 1) + "_" + data_type  + "_ignore_prior"
print("result file is : ",resultFile)
if not os.path.exists(resultFile) or replace_flag:
	print("calling NB classifier ",expFol,str(time_window+1),data_type)
	dataList = np.genfromtxt("timestamp_" + data_type,dtype='str')
	dataList = np.unique(dataList)
	def callNB(fold,dataList,expFol,time_window,data_type):
		for data in dataList:
			print("data = ",fold,data)
			resultFile = expFol + "/fold" + str(fold) + "/" + data + "/result_" + str(time_window + 1) + "_" + data_type  + "_ignore_prior"
			trainPath = expFol + "/fold" + str(fold) + "/" + data + "/train_tweets_" + str(time_window + 1) + "_" + data_type
			testPath = expFol + "/fold" + str(fold) + "/" + data + "/test_tweets_" + str(time_window + 1) + "_" + data_type
			try:
				if nb_type == "mw":
					naiveBayesNPP_onlyMaxWord.classify(trainPath,testPath,resultFile,city_format_file,0.1)
				else:	
					naiveBayesNPP_prior.classify(trainPath,testPath,resultFile,city_format_file,0.1)
			except Exception as e:
				print("[callNB]got error: ",e,resultFile,trainPath,testPath)
				exc_type, exc_obj, exc_tb = sys.exc_info()
				fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
				print("[callNB] ",exc_type, fname, exc_tb.tb_lineno)
				continue 
	procs = []
	for f in range(1,11):
		proc = Process(target=callNB, args=(f,dataList,expFol,time_window,data_type))
		procs.append(proc)
		proc.start()
	for proc in procs:
		proc.join()

#-----merge_results-----

merge_results(expFol,str(time_window+1),data_type,final_output)

print("Done")
