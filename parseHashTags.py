import csv
import re
import pandas as pd

def extHashtag(s):
	return re.findall(r"#(\w+)", s) 

ipf = open("tweetData/tweet_text1.csv","r")
opf = open("tweetData/full_hashtags","w")

tweet_id_list = pd.read_csv("tweetData/tweet_info.csv",header=None)
vList = tweet_id_list.values

count = 0
for line in ipf:
	
	ht = extHashtag(line)
	if len(ht) <= 0:
		count+=1 
		continue
	print("count = ",count)
	opf.write(" ".join(ht) + "," + ",".join([str(x) for x in vList[count]]) + "\n")
	count+=1
	#if count > 100: break
print("Done, count = ",count)

