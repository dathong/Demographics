import tweepy
from tweepy import Stream
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
import time
# from appMng import rotateApp
# from appMng import appMng
import appMng
import pandas as pd
import os
import json



def getUserInfo(userList):

   #output folder to store user profile information
   fol = "user_profile/"
   finishedList = "./user_profile/finishedList.csv"
   
   fnFile = open(finishedList,"a")

   #rotate token information so if one token exceeded the limit, we will switch to another one
   (CONSUMER_KEY,CONSUMER_SECRET,ACCESS_KEY,ACCESS_SECRET) = appMng.appMng(2)
   auth = OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
   api = tweepy.API(auth)
   auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
   userCount = len(userList)
   print("len userList: ",str(userCount))
   
   index = 0


   #craw each user in the list
   while index < userCount:

      user_name = userList[index]
      try:
         print("trying to collect user ", user_name)
         test = api.lookup_users(screen_names= [user_name])
         #crawl succesfully, prepare to store the profile in the file
         for i,user in enumerate(test):
          with open(fol + user.screen_name  + ".csv","w") as f:
       
            print("output for user ",user.screen_name)
    
            # dumpt to json
            json.dump(user._json, f)
            index+=1
     
            print("index = ",index)
          fnFile.write(user.screen_name + ".csv \n")

      except Exception as e:
         print("error at index ",e,index)
         if 'Not authorized' in str(e) or 'No user matches' in str(e):
             print("returning... bkup user ",user_name)
             fnFile.write(user_name + ".csv \n")
             index+=1
             continue
         time.sleep(60)

if __name__ == "__main__":

  #before crawling, get all the finished users so we don't crawl these users again
  finishedList = pd.read_csv("./user_profile/finishedList.csv",header=None).values.tolist() 
  finishedList = [x[0] for x in finishedList]

  #read the original list of users we want to crawl
  dfUserList = pd.read_csv("Unique.csv",header=None)
  fullList = dfUserList[0].values.tolist()

  #filter only the users we will crawl
  userList = [u for u in fullList if u not in finishedList]
  print("user List = ", userList[:10])
  #begin crawling
  getUserInfo(userList)
  print("Done")
  
