import pandas as pd
import numpy as np
import json

col_list = ['user_id','tweet_id','handle','time_stamp','full_tweet','location','coordinates','city_flag','retweet_flag','hash_tags','xxx','nouns']

#--get city lis---
lines = open("tweetIAFormatFull","r").readlines()[0]
city_list = lines.split("|")
locs = city_list[6:]

df = pd.read_csv('tweetIA_Noun.csv',names=col_list,index_col=False)

df['time_stamp'] = df['time_stamp'].str.split(" ").str[0].replace(" ","_")
df = df[df.location.isin(locs)]
#:noh
#df = df[~df['hash_tags'].isnull()]
df = df[~df['nouns'].isnull()]
#df1 = df1[~df1['cityFlag'].isnull()]
#df1['location'] = df1['location'].str.replace(",","").str.replace(" ","_").str.lower()
df['nouns'] = df['nouns'].str.replace(","," ").str.lower()
#df['hash_tags'] = df['hash_tags'].str.replace(","," ").str.lower()

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

#df['timestamp'] = df['timestamp'].apply(lambda x: changeDate(x))
#df['time_stamp'] = df['time_stamp'].apply(lambda x: changeDate1m(x))
df.to_csv("tweets_data_processed_1day_nouns.csv",sep="|")
dayDf = pd.read_csv("tweets_data_processed_1day_nouns.csv",sep="|")
np.savetxt("timestamp_1day_nouns",dayDf['time_stamp'].unique() ,newline="\n",fmt='%s')

