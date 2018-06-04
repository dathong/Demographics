import os
import pandas as pd
import json
import numpy as np
import math
import operator
import sys
import pickle


def save_obj(obj, name ):
	with open(name + '.pkl', 'wb') as f:
		pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
	with open(name + '.pkl', 'rb') as f:
		return pickle.load(f)

def classify(trainFile,testFile,resultFile,t):
# inputFile = "train_txt_data.csv"
	print('nb intep training....')
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

	for r in df[1].values:
		for w in r.split():
			if w not in wordDict:
				wordDict[w] = {}
				for c in classList:
					wordDict[w][c] = 1


	for c in classList:
    # print("--c = ",c)
		dfX = df[df[2] == c]

		class_prob[c] = dfX.shape[0]/N
		for r in dfX[1].values:
        # print("---r = ",r)
			for w in r.split():

				wordDict[w][c]+=1
            # print("----wordDict = ",wordDict)
				classDict[c] +=1

	for w in wordDict:
		for c in classDict:
			wordDict[w][c]/=(classDict[c] + len(wordDict))

	wordDict_pos = {}
	for w in wordDict:
		p_w = 0
		wordDict_pos[w] = {}
		for c in wordDict[w]:
			p_w += wordDict[w][c]*class_prob[c]
			
		for c in class_prob:
			wordDict_pos[w][c] = wordDict[w][c]*class_prob[c]/(p_w)

# print("class_prob: ",class_prob)
# print("wordDict = ",wordDict)
# print("classDict = ",classDict)
	print('NB intep testing....')

	dicElems = resultFile.split("/")
	storeDic = "/".join([s for s in dicElems[:len(dicElems) - 1]]) 

	with open(storeDic + "/"+ 'class_prob.json', 'w') as fp:
		json.dump(class_prob, fp)
		save_obj(class_prob,storeDic + "/"+ 'class_prob')
	with open(storeDic + "/"+ 'wordDict.json', 'w') as fp:
		json.dump(wordDict, fp)
		save_obj(wordDict,storeDic + "/"+ 'wordDict')
	with open(storeDic + "/"+ 'wordDict_pos.json', 'w') as fp:
		json.dump(wordDict_pos, fp)
		save_obj(wordDict,storeDic + "/"+ 'wordDict_pos')
	with open(storeDic + "/"+ 'classDict.json', 'w') as fp:
		json.dump(classDict, fp)
		save_obj(classDict,storeDic + "/"+ 'classDict')
# print("probDict = ",probDict)


#fTest = open("df112.csv","r",encoding="ascii")
	fTest = pd.read_csv(testFile,header=None)
#fTest = pd.read_csv("df112.csv",header=None,nrows=10000000)
#print("fTest = ",fTest)
	testList = fTest[1]
	idList = fTest[0]
#print("testDf = ",testList)

	predProb = {}
	predProbOne = {}
	resultOp = open(resultFile,"w")
	resultOp.write("|".join(["id","pred_lbl","pred_prob","prior_prob","prior_lbl","max_comp_lbl","max_comp","max_comp_prob","unk"]) + "\n")
	logRes = []
	class_prob_log = {}
	for item in class_prob:
		class_prob_log[item] = math.log(class_prob[item])
	for i,x in enumerate(testList):
		unkFlag = 1
		maxLocs = []
		for c in classDict:
			predProb[c] = math.log(class_prob[c])
			predProbOne[c] = class_prob[c]
			maxComp = np.array([None,float('-inf')])
			for w in x.split():
				if w not in wordDict: continue
				predProb[c] += math.log(wordDict[w][c])
				unkFlag = 0
				if wordDict_pos[w][c] > maxComp[1]: 
					maxComp[0] = w
					maxComp[1] = wordDict_pos[w][c]
			maxLocs.append([c,maxComp[0],maxComp[1]])
		maxLocs = np.array(maxLocs)
		maxLocsSorted = maxLocs[maxLocs[:,2].argsort()]
		sorted_x = sorted(predProb.items(), key=operator.itemgetter(1),reverse=True)
		sorted_prior = sorted(class_prob_log.items(), key=operator.itemgetter(1),reverse=True)
		predRes = sorted_x[0][0]
		predCity = sorted_prior[0][0]
		resultOp.write("|".join([str(idList[i]),str(sorted_x[0][0]),str(sorted_x[0][1]),str(sorted_prior[0][1]),sorted_prior[0][0],str(maxLocsSorted[-1][0]),str(maxLocsSorted[-1][1]),str(maxLocsSorted[-1][2]),str(unkFlag)]) + "\n")

if __name__ == "__main__":
	
	#classify("df111.csv","df112.csv","resultOp.csv")
	classify("train_txt_data.csv","test_txt_data.csv","./result_txt.csv",0.1)
	#print("Done")
	
	
	sys.exit()
	expFol = sys.argv[1]
	time = sys.argv[2]
	datType = sys.argv[3]
	
	dataList = np.genfromtxt("timestamp_" + time + "_" + datType,dtype='str')
	for fold in range(1,11):
	
		for data in dataList:
			print("data = ",fold,data)
			resultFile = expFol + "/fold" + str(fold) + "/" + data + "/result_" + time + "_" + datType + "_intep"
			trainPath = expFol + "/fold" + str(fold) + "/" + data + "/train_tweets_" + time + "_" + datType
			testPath = expFol + "/fold" + str(fold) + "/" + data + "/test_tweets_" + time + "_" + datType
			try:
				classify(trainPath,testPath,resultFile,0.1)
			except Exception as e:
				print("got error: ",e)
				continue
	print("Done")
