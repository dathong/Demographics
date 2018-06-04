#!/usr/bin/env python
# encoding: utf-8
import json
import pprint
import tweepy #https://github.com/tweepy/tweepy
import csv
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()
import time
import ast
from twitter import *
import os, errno
import pandas as pd

#Twitter API credentials
consumer_key = "i4ReUBPhLUFNlGYfk5wBDZaAl"
consumer_secret = "YGe1TfIlBeo3DSKZ6cKzX5hD8Pkw3Pdgfv1OYKhSP2Z4fbZVyS"
access_key = "1973722680-GJon8YENN4i8FLOYxypXaMASlUfriceRZKXGj0r"
access_secret = "H5xnyIJ410E4qRjfIuS0fJYIxIbZ40aQJaRPAkh6UlPou"
fol = "user_tweets/"

def get_all_tweets(screen_name):
    #Twitter only allows access to a users most recent 3240 tweets with this method
    
    #authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    
    #initialize a list to hold all the tweepy Tweets
    alltweets = []    
    
    #make initial request for most recent tweets (200 is the maximum allowed count)
    while True:
       try:
          new_tweets = api.user_timeline(user_id = screen_name,count=200)         ###NOTE
          break
       except tweepy.TweepError as e:
          print("some errors...",e)
          print("class e: ",e.api_code)
          if e.api_code == 34 or 'Not authorized' in str(e):
              print("returning for user..." + str(screen_name))
              return
          time.sleep(60)
    #save most recent tweets
    alltweets.extend(new_tweets)
    #print new_tweets
    #save the id of the oldest tweet less one
    if len(alltweets) == 0: return
    oldest = alltweets[-1].id - 1
    print (oldest)
    #keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        print ("getting tweets before %s" % (oldest))
        
        #all subsiquent requests use the max_id param to prevent duplicates
        while True:
            try:    
                new_tweets = api.user_timeline(user_id = screen_name,count=200,max_id=oldest) #default count = 20
                break
            except tweepy.TweepError as e:
                print("some errors...",e)
                print("class e: ",e.api_code)
                if e.api_code == 34 or 'Not authorized' in str(e):
                  print("returning for user " + str(screen_name))
                  return
                time.sleep(60) 
        #save most recent tweets
        alltweets.extend(new_tweets)
        
        #update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1
        
        print ("...%s tweets downloaded so far" % (len(alltweets)))
    #$print json.loads(alltweets[0])
    pprint.pprint(str(alltweets[0]).encode("utf-8"))
    
    
    #transform the tweepy tweets into a 2D array that will populate the csv    
    outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in alltweets]
    
    
    #print outtweets[0]
    
    
    #write the csv    
    with open(fol + '%s.csv' % screen_name, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(["id","created_at","text"])
        writer.writerows(outtweets)
    
    pass

if __name__ == '__main__':
    # pass in the username of the account you want to download
    df = pd.read_csv("./kaggle_data/gender-classifier-DFE-791531.csv",encoding='latin1')
    userList = df['_unit_id'].values.tolist()
    for uid in userList:
      get_all_tweets(uid)
    print("Done")
