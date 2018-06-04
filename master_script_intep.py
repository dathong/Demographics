#----
# Written by Dat Hong
#-----
import pandas as pd
import numpy as np
import json
import os
from sklearn.model_selection import KFold
from sklearn import cross_validation
import naiveBayesNPP_prior
import naiveBayesNPP_onlyMaxWord
import naiveBayes_intep
import merge_results
import merge_result_intep
import sys


#----input params----
# Here are where we need to change:
# +expFol: the directory we want to export everything into
# +final_output: the name of the final output file
# +data_type: 'hash_tags' or 'nouns'
# +city_format_file: the state city format file, generated by Jon
# +input_csv_file: the input csv file generated by Osama
# +user_fold_file: the 10-fold user list file generated by Osama
# +nb_type: 'normal' for normal Naive Bayes or 'mw' for max-word only
# +time_window: 0 means no span time window, 1 means 1-day forward and 1-day backward,...
# After finishing, the output file would be in expFol dir
# Please let me know if you have any questions.
#-----
#state = "IA"
state = sys.argv[1]
print("param state = ",state)
#expFol = "test_master_script"
#expFol = state + "_output/"
replace_flag = True
delete_folds = True
#replace_flag = False
date_cutoff = '2016-12-10'
#time_window = 0 #1,2,3
time_window = int(sys.argv[2])
print("time_window = ",time_window)
#data_type = "hash_tags"
#data_type = "nouns"
data_type = sys.argv[3]
print("data_type = ",data_type)
city_format_file = "states_data/fullFormats/tweet" + state + "FormatFull"
input_csv_file = "states_data/tweet" + state + "_Hash.csv"
if data_type == "nouns":
	input_csv_file = "states_data/tweet" + state + "_Noun.csv"
row_num = 10000000
user_fold_file = "states_data/Folds/Fold" + state + ".csv"
final_output = "final_tweets_" + str(int(time_window)+1) + "_" + data_type + "_" + str(state) + ".csv"
#nb_type = "normal" # "normal" or "mw" or "intep"
nb_type = sys.argv[4]
print("nb_type = ",nb_type)
expFol = state + "_output/" + str(2*time_window+1) + "_" + data_type + "_" + nb_type
col_list = ['user_id','tweet_id','handle','time_stamp','full_tweet','location','coordinates','city_flag','retweet_flag','hash_tags','has_hash_tags','nouns','has_nouns']
final_output = "final_tweets_" + str(2*int(time_window)+1) + "_" + data_type + "_" + str(state) + "_" + nb_type + ".csv"
#----
#----temp files ------
if not os.path.exists(expFol):
	    os.makedirs(expFol)
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
	#df = df[~df['hash_tags'].isnull()]
	df = df[~df[data_type].isnull()]
	#df1 = df1[~df1['cityFlag'].isnull()]
	#df1['location'] = df1['location'].str.replace(",","").str.replace(" ","_").str.lower()
	df[data_type] = df[data_type].str.replace(","," ").str.lower()
#df['hash_tags'] = df['hash_tags'].str.replace(","," ").str.lower()
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

	def changeDate2w(col):
		dates = col.split(" ")[0].split("-")
		year = dates[0]
		month = dates[1]
		day = dates[2]
		if int(day) < 15:
			day = "w12"
		else:
			day = "w34"
		return "_".join([str(year),str(month),str(day)])

	def changeDate1w(col):
		dates = col.split(" ")[0].split("-")
		year = dates[0]
		month = dates[1]
		day = dates[2]
		if int(day) <= 7:
			day = "w1"
		elif 7 < int(day) and int(day) <= 14:
			day = "w2"
		elif 14 < int(day) and int(day) <= 21:
			day = "w3"
		else:
			day = "w4"
		return "_".join([str(year),str(month),str(day)])


	def changeDate1m(col):
		dates = col.split(" ")[0].split("-")
		year = dates[0]
		month = dates[1]
		day = dates[2]
		return "_".join([str(year),str(month)])

	df.to_csv(processed_csv_file,sep="|") 

dayDf = pd.read_csv(processed_csv_file,sep="|")
np.savetxt(expFol + "/timestamp_" + data_type,dayDf['time_stamp'].unique() ,newline="\n",fmt='%s')
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
			print("dates & shape = ",date,df2testX.shape)
			df2testX.to_csv(dts + "test_tweets_" + str(time_window + 1) + "_" + data_type,header=None,index=None)

#---run NB classifier----
fold = 2
dataList = np.genfromtxt(expFol + "/timestamp_" + data_type,dtype='str')
dataList = np.unique(dataList)
#expFol = str(time_window + 1) + "_" + data_type
resultFile = expFol + "/fold" + str(fold) + "/" + dataList[1] + "/result_" + str(time_window + 1) + "_" + data_type  + "_ignore_prior"
print("result file is : ",resultFile)
if not os.path.exists(resultFile) or replace_flag:
	print("nb_NPP_prior ",expFol,str(time_window+1),data_type)
	dataList = np.genfromtxt(expFol + "/timestamp_" + data_type,dtype='str')
	dataList = np.unique(dataList)
	for fold in range(1,11):
		for data in dataList:
			print("data = ",fold,data)
			resultFile = expFol + "/fold" + str(fold) + "/" + data + "/result_" + str(time_window + 1) + "_" + data_type  + "_ignore_prior"
			trainPath = expFol + "/fold" + str(fold) + "/" + data + "/train_tweets_" + str(time_window + 1) + "_" + data_type
			testPath = expFol + "/fold" + str(fold) + "/" + data + "/test_tweets_" + str(time_window + 1) + "_" + data_type
			try:
				if nb_type == "mw":
					naiveBayesNPP_onlyMaxWord.classify(trainPath,testPath,resultFile,city_format_file,0.1)
				elif nb_type == "intep":
					naiveBayes_intep.classify(trainPath,testPath,resultFile,0.1)
				else:
					naiveBayesNPP_prior.classify(trainPath,testPath,resultFile,city_format_file,0.1)

			except Exception as e:
				print("got error: ",e)
				continue 
#-----merge_results-----

print("nb_type x = ",nb_type)
if nb_type == "intep":
	merge_result_intep.merge_results(expFol,str(time_window+1),data_type,final_output)
else:
	merge_results.merge_results(expFol,str(time_window+1),data_type,final_output)
#----delete folds to save space----

import shutil

if delete_folds:
	print("deleting...")
	for i in range(1,11):
		print("deleting fold..",i)
		shutil.rmtree(expFol + '/fold' + str(i))

print("Done")
