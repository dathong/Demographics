#!/usr/bin/env python
# encoding: utf-8

import tweepy #https://github.com/tweepy/tweepy
import csv
import time
import ast
from twitter import *
#Twitter API credentials
        
consumer_key = ""
consumer_secret = ""
access_key = ""
access_secret = ""
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

import tweepy
import json

    
CityHandle=open("USmilTweet.csv", "w")
# This is the listener, resposible for receiving data
class StdOutListener(tweepy.StreamListener):
    def __init__(self, api=None):
        super(StdOutListener, self).__init__()
        self.num_tweets = 0
    
    def on_data(self, data):
        # Twitter returns data in JSON format - we need to decode it first
        decoded = json.loads(data)
        
        # Also, we convert UTF-8 to ASCII ignoring all bad characters sent by users
        Str= decoded['place']['bounding_box']['coordinates']
        Coords= str(Str).split('], [')[0].replace("[","")
        #print Str[0]
        place=decoded['place']['full_name'].find('IA')
        title= decoded['place']['full_name']
        print title
        print '@%s: %s' % (decoded['user']['screen_name'], decoded['text'].encode('ascii', 'ignore'))
        CityHandle.write(decoded['user']['screen_name']+','+title+','+Coords+"\n")
        print ''
        self.num_tweets += 1
        if self.num_tweets < 1000000:
            return True
        else:
            return False

    def on_error(self, status):
        print status

if __name__ == '__main__':
    global i
    l = StdOutListener()
    i=0    
    print "Showing all new tweets for #programming:"
    LOCATIONS = [-124.7771694, 24.520833, -66.947028, 49.384472,     # Contiguous US 
                 -164.639405, 58.806859, -144.152365, 71.76871,      # Alaska 
                 -160.161542, 18.776344, -154.641396, 22.878623]     # Hawaii 
    # There are different kinds of streams: public stream, user stream, multi-user streams
    # In this example follow #programming tag
    # For more details refer to https://dev.twitter.com/docs/streaming-apis
    if i < 10:
        stream = tweepy.Stream(auth,l,count = 2)
        j=0
        while True:
            j=j+1
            try:
                #stream.filter(locations=[-180,-90,180,90]) #Entire World
                #stream.filter(query="Iowa")
                stream.filter(locations=LOCATIONS)
                break
            except:
                print "Wait"
                time.sleep(1)
                
            
        #stream.filter(locations=[-91.320529,40.842275,-95.828434,43.371824])
    
    