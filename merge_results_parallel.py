import pandas as pd
import numpy as np
import sys
import os
from multiprocessing import Process
#eFol = sys.argv[1]
#time = sys.argv[2]
#datType = sys.argv[3]

def merge_results(eFol,time,datType,final_output):
	print("merging results...")
	dataList = np.genfromtxt("timestamp_" + datType,dtype='str')
	mergeDf = pd.DataFrame()
	expFol = eFol + "/"
	result_file = "/result_" + time + "_" + datType + "_ignore_prior"
	test_tweets_full = "/test_tweets_full_" + time + "_" + datType
	test_tweets_full_merged = "/test_tweets_full_"  + time + "_" + datType + "_merged"
	final_tweets = expFol + final_output
	
	print("final_tweets = ",final_tweets)
	if os.path.exists(final_tweets):
		return
	print("proceeding...")
	for fold in [2]:
		for data in dataList[2:4]:
			print("data = ",fold,data)
			resultFile = expFol + "fold" + str(fold) + "/" + data + result_file
			fullText = expFol + "fold" + str(fold) + "/"+ data + test_tweets_full
			exportPath = expFol + "fold" + str(fold) + "/" + data + test_tweets_full_merged
			df1 = pd.read_csv(resultFile,sep="|")
			df2 = pd.read_csv(fullText)
			df = pd.concat([df2, df1], axis=1)
			df.drop(['Unnamed: 0','user_id','full_tweet','has_hash_tags','has_nouns','retweet_flag','city_flag','time_stamp','hash_tags', df.columns.values[-1]], axis=1, inplace=True)
			df.rename(columns={'coordinates':'GroundTruthCoordinate','location':'GroundTruthCity'},inplace=True)
			#---change columns----
			c = df.columns.values.tolist()
			if 'retweet_flag' in c:
				c.remove('retweet_flag')
			if 'IgnoreFlag' in c:
				c.remove('IgnoreFlag')  
			if 'nouns' in c:
				c.remove('nouns')
			c = ['IgnoreFlag'] + c
			df = df[c]
			#---
			df.to_csv(exportPath,index=False)
			colList = df.columns.values
			print("colList = ",colList)
			# np.savetxt("finalTweets2.csv",colList,fmt="%s",delimiter="|",newline='|')
			with open(final_tweets,"w") as f:
				f.write("|".join(colList) + "\n")
			break

	
	def merging_results(fold,dataList,result_file,test_tweets_full,test_tweets_full_merged):
		for data in dataList:
			print("data = ",fold,data)
			try: 
				resultFile = expFol + "fold" + str(fold) + "/" + data + result_file
				fullText = expFol + "fold" + str(fold) + "/"+ data + test_tweets_full
				exportPath = expFol + "fold" + str(fold) + "/" + data + test_tweets_full_merged
				df1 = pd.read_csv(resultFile,sep="|")
				df2 = pd.read_csv(fullText)
				df = pd.concat([df2, df1], axis=1)
				#df.drop(labels=df.columns.values[-1], axis=1,inplace=True)
				df.drop(['Unnamed: 0','user_id','full_tweet','has_hash_tags','has_nouns','retweet_flag','city_flag','time_stamp','hash_tags', df.columns.values[-1]], axis=1, inplace=True)
				df.rename(columns={'coordinates':'GroundTruthCoordinate','location':'GroundTruthCity'},inplace=True)
				#df['IgnoreFlag'] = 0
				#---change columns---
				c = df.columns.values.tolist()
				if 'retweet_flag' in c:
					c.remove('retweet_flag')
				if 'IgnoreFlag' in c:
					c.remove('IgnoreFlag')
				if 'nouns' in c:
					c.remove('nouns')
				c = ['IgnoreFlag'] + c
				df = df[c]
				#---
				df.to_csv(exportPath,index=False)
				df.to_csv(final_tweets, mode="a",header=False,index=False,sep="|")
			except Exception as e:
				print("got error: ",e)
				continue
	procs = []	        
	for fold in range(1,11):
		proc = Process(target=merging_results, args=(fold,dataList,result_file,test_tweets_full,test_tweets_full_merged))
		procs.append(proc)
		proc.start()
