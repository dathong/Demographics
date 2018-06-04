#!/usr/bin/env python
# encoding: utf-8

import tweepy  # https://github.com/tweepy/tweepy
import csv
import pandas as pd
import time

# Twitter API credentials
# ACCESS_TOKEN = '1973722680-GJon8YENN4i8FLOYxypXaMASlUfriceRZKXGj0r'
# ACCESS_SECRET = 'H5xnyIJ410E4qRjfIuS0fJYIxIbZ40aQJaRPAkh6UlPou'
# CONSUMER_KEY = 'i4ReUBPhLUFNlGYfk5wBDZaAl'
# CONSUMER_SECRET = 'YGe1TfIlBeo3DSKZ6cKzX5hD8Pkw3Pdgfv1OYKhSP2Z4fbZVyS'
consumer_key = "i4ReUBPhLUFNlGYfk5wBDZaAl"
consumer_secret = "YGe1TfIlBeo3DSKZ6cKzX5hD8Pkw3Pdgfv1OYKhSP2Z4fbZVyS"
access_key = "1973722680-GJon8YENN4i8FLOYxypXaMASlUfriceRZKXGj0r"
access_secret = "H5xnyIJ410E4qRjfIuS0fJYIxIbZ40aQJaRPAkh6UlPou"
fol = "user_tweets/"

def get_all_tweets(uid):
    # Twitter only allows access to a users most recent 3240 tweets with this method
    print("user = ",uid)
    # authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    # initialize a list to hold all the tweepy Tweets
    alltweets = []

    # make initial request for most recent tweets (200 is the maximum allowed count)
    #new_tweets = api.user_timeline(screen_name=screen_name, count=200)
    while True:
       try:
          
          new_tweets = api.user_timeline(user_id=uid , count=200) 
          break
       except tweepy.TweepError as e:
          print("some errors...",e)
          print("class e: ",e.api_code)
          if e.api_code == 34 or 'Not authorized' in str(e):
             print("returning...")
             return
          time.sleep(60)
    # save most recent tweets
    alltweets.extend(new_tweets)
    if len(alltweets) == 0:
       print("len tweet is 0")
       return
    # save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1

    # keep grabbing tweets until there are no tweets left to grab
    count = 1
    maxCount = 5
    while len(new_tweets) > 0 and count <= maxCount:
        print("getting tweets before %s" % (oldest))

        # all subsiquent requests use the max_id param to prevent duplicates
        #new_tweets = api.user_timeline(screen_name=screen_name, count=200, max_id=oldest)
        #new_tweets = api.user_timeline(user_id=uid, count=200)
        while True:
          try:

             new_tweets = api.user_timeline(user_id=uid , count=200)
             break
          except tweepy.TweepError as e:
             print("some errors...",e)
             print("class e: ",e.api_code)
             if e.api_code == 34 or 'Not authorized' in str(e):
                print("returning...")
                return
             time.sleep(60)
        # save most recent tweets
        alltweets.extend(new_tweets)

        # update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

        print("...%s tweets downloaded so far" % (len(alltweets)))
        count+=1
    # transform the tweepy tweets into a 2D array that will populate the csv
    outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in alltweets]

    # write the csv
    print("writing to ",fol + '%s_tweets.csv' % uid)
    with open(fol + '%s_tweets.csv' % uid, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(["id", "created_at", "text"])
        writer.writerows(outtweets)
    
    pass


if __name__ == '__main__':
    # pass in the username of the account you want to download
    df = pd.read_csv("./kaggle_data/gender-classifier-DFE-791531.csv",encoding='latin1')
    userList = df['_unit_id'].values.tolist()
    for uid in userList:
       get_all_tweets(uid)
