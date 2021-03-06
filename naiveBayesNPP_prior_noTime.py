import os
import pandas as pd
import json
import numpy as np
import math
import operator
import sys

def probNormalize(dic):
	res = {}
	for elem in dic:
		res[elem] = dic[elem]/sum(dic.values())
	return res

def npIndexOf(array,value):
	return np.where(array == value)[0][0]


def classify(trainFile,testFile,resultFile,t):
# inputFile = "train_txt_data.csv"
	print('training....')
	#inputFile = "df111.csv"
	#inputFile = "train_txt_data.csv"
	df = pd.read_csv(trainFile,header=None,nrows=10000000)

	#print(df)
	N = df.shape[0]

	classList = df[1].unique()

	class_prob = {}
	classDict = {}
	probDict = {}
	for c in classList:
		classDict[c] = 0
	wordDict = {}

	for r in df[0].values:
		for w in r.split():
			if w not in wordDict:
				wordDict[w] = {}
				for c in classList:
					wordDict[w][c] = 1


	for c in classList:
	# print("--c = ",c)
		dfX = df[df[1] == c]

		class_prob[c] = dfX.shape[0]/N
		for r in dfX[0].values:
		# print("---r = ",r)
			for w in r.split():

				wordDict[w][c]+=1
			# print("----wordDict = ",wordDict)
				classDict[c] +=1

	for w in wordDict:
		for c in classDict:
			wordDict[w][c]/=(classDict[c] + len(wordDict))

	print('testing....')


	with open('class_prob.json', 'w') as fp:
		json.dump(class_prob, fp)
	with open('wordDict.json', 'w') as fp:
		json.dump(wordDict, fp)
	with open('classDict.json', 'w') as fp:
		json.dump(classDict, fp)
# print("probDict = ",probDict)


	fTest = pd.read_csv(testFile,header=None)
	testList = fTest[0]

	predProb = {}
	resultOp = open(resultFile,"w")
	
	fullCols = np.array(open("tweetALFormatFull","r").read().split("|")) 

	#fixedColArr = np.array(['pred_lbl','pred_prob','prior_prob','prior_lbl'])
	fixedColArr = fullCols[:6]
	lblArr = fullCols[6:]
	#lblArr = np.array(['j','v','c'])

	resultOp.write("IgnoreFlag|PriorCity|" +  "|".join(map(str,lblArr)) + "\n")
	logRes = []
	class_prob_log = {}
	for item in class_prob:
		class_prob_log[item] = math.log(class_prob[item])
	for i,x in enumerate(testList):
		noTrainingData = "1"
		predArr = np.zeros(lblArr.shape[0])
		for c in classDict:
			predArr[npIndexOf(lblArr,c)] = class_prob[c]
			for w in x.split():
				if w not in wordDict: continue
				else:
					noTrainingData = "0"
					predArr[npIndexOf(lblArr,c)] *= wordDict[w][c]
		predArr = predArr/sum(predArr)
		#print("predProb after normalizing = ",predArr) 
		sorted_prior = sorted(class_prob.items(), key=operator.itemgetter(1),reverse=True)
		predMaxProb =  max(predArr)
		predMaxInd = np.where(predArr == predMaxProb)[0][0]
		predRes = lblArr[predMaxInd]
		resultOp.write(noTrainingData + "|")
		resultOp.write(str(sorted_prior[0][0]) + "|")
		resultOp.write("|".join(map(str,predArr)) + "\n")

if __name__ == "__main__":
	

	#classify("df111.csv","df112.csv","resultOp.csv")
	#classify("train_txt_data.csv","test_txt_data.csv","result_test.csv",0.1)
	#print("Done")
	
	
	#sys.exit()
	#expFol = "1d_nouns"
	#time = "1day"
	#datType = "nouns"
	expFol = sys.argv[1]
	time = sys.argv[2]
	datType = sys.argv[3]
	
	print("nb_NPP_prior ",expFol,time,datType)

	dataList = np.genfromtxt("timestamp_" + time + "_" + datType,dtype='str')
	dataList = np.unique(dataList)
	#dataList = ['2017-11-07','2017-11-06','2017-11-05','2017-11-04','2017-11-03']
	for fold in range(1,11):
			print("fold = ",fold)
			resultFile = expFol + "/fold" + str(fold) + "/result_" + time + "_" + datType  + "_ignore_prior"
			trainPath = expFol + "/fold" + str(fold) + "/train_tweets_" + time + "_" + datType
			testPath = expFol + "/fold" + str(fold) + "/test_tweets_" + time + "_" + datType
			try:
				classify(trainPath,testPath,resultFile,0.1)
			except Exception as e:
				print("got error: ",e)
				continue
	print("Done")
