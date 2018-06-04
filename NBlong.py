import os
import pandas as pd
import json
import numpy as np
import math
import operator
import sys


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def probNormalize(dic):
	res = {}
	count = 0
	sumVal = 0
	for elem in dic:
		if is_number(dic[elem]):
			count+=1
			sumVal+= float(dic[elem])
	for elem in dic:
		if is_number(dic[elem]):
			res[elem] = float(dic[elem])/sumVal
		else:
			res[elem] = float('nan')
	
	return res

def classify(trainFile,testFile,resultFile,t):
	
	print('training....')
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

# print("class_prob: ",class_prob)
# print("wordDict = ",wordDict)
# print("classDict = ",classDict)
	print('testing....')


	with open('class_prob.json', 'w') as fp:
		json.dump(class_prob, fp)
	with open('wordDict.json', 'w') as fp:
		json.dump(wordDict, fp)
	with open('classDict.json', 'w') as fp:
		json.dump(classDict, fp)
# print("probDict = ",probDict)


#fTest = open("df112.csv","r",encoding="ascii")
	fTest = pd.read_csv(testFile,header=None)
#fTest = pd.read_csv("df112.csv",header=None,nrows=10000000)
#print("fTest = ",fTest)
	testList = fTest[0]
#print("testDf = ",testList)

	predProb = {}
	#----load locations-----
	locationList = json.load(open("locations.json","r"))
	#locationList = ['c','n','j','m']
	for l in locationList:
		predProb[l] = 'no_val'
		
	#----

	
	resultOp = open(resultFile,"w")
	resultOp.write(",".join(["pred_lbl","pred_prob","prior_prob","prior_lbl"]) + ",")
	sorted_classDict = sorted(predProb.items(), key=operator.itemgetter(0),reverse=True)
	for elem in sorted_classDict:
		resultOp.write(str(elem[0]) + ",")
	resultOp.write("\n")
	logRes = []
	class_prob_log = {}
	for item in class_prob:
		class_prob_log[item] = math.log(class_prob[item])
	for i,x in enumerate(testList):
		for c in classDict:
			predProb[c] = class_prob[c]
			for w in x.split():
				if w not in wordDict: continue
				predProb[c] *= wordDict[w][c]
		#print("predProb before normalizing = ",predProb) 
		resPredProb = probNormalize(predProb)
		#print("predProb after normalizing = ",resPredProb) 
		sorted_x = sorted(resPredProb.items(), key=operator.itemgetter(1),reverse=True)
		sorted_prior = sorted(class_prob.items(), key=operator.itemgetter(1),reverse=True)
		predRes = sorted_x[0][0]
		predCity = sorted_prior[0][0]
		resultOp.write(",".join([str(sorted_x[0][0]),str(sorted_x[0][1]),str(sorted_prior[0][1]),sorted_prior[0][0]]) + ",")
		sorted_predProb = sorted(resPredProb.items(), key=operator.itemgetter(0),reverse=True)
		for elem in sorted_predProb:
			resultOp.write(str(elem[1]) + ",")
		resultOp.write("\n")

if __name__ == "__main__":
	
	#classify("train_txt_data.csv","test_txt_data.csv","result_txt.csv",0.1)
	#print("Done")
	
	
	#sys.exit()
	dataList = np.genfromtxt('exp1/timestamp',dtype='str')
	#dataList = ['2017-11-07','2017-11-06','2017-11-05','2017-11-04','2017-11-03']
	for fold in range(1,11):
		for data in dataList:
			print("data = ",fold,data)
			resultFile = "exp1/fold" + str(fold) + "/" + data + "/resultFile2.csv" 
			trainPath = "exp1/fold" + str(fold) + "/" + data + "/train_tweets"
			testPath = "exp1/fold" + str(fold) + "/" + data + "/test_tweets"
			try:
				classify(trainPath,testPath,resultFile,0.1)
			except Exception as e:
				print("got error: ",e)
				continue
	print("Done")
