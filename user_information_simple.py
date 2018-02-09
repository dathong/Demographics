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


class TweetListener(StreamListener):
    # A listener handles tweets are the received from the stream.
    #This is a basic listener that just prints received tweets to standard output

    def on_data(self, data):
        print (data)
        return True

    def on_error(self, status):
        print (status)



def getUserInfo(userList):
   fol = "user_profile/"
   finishedList = "./user_profile/finishedList.csv"
   
   fnFile = open(finishedList,"a")
   (CONSUMER_KEY,CONSUMER_SECRET,ACCESS_KEY,ACCESS_SECRET) = appMng.rotateApp()
   auth = OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
   api = tweepy.API(auth)
   auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
   userCount = len(userList)
   print("len userList: ",str(userCount))
   #test = api.lookup_users(screen_names= userList)
   
   index = 0

   while index < userCount:

      user_name = userList[index]
      try:
         print("trying to collect user ", user_name)
         test = api.lookup_users(screen_names= [user_name])
         for i,user in enumerate(test):
          with open(fol + user.screen_name  + ".csv","w") as f:
       
            print("writing for user ",user.screen_name)
            # userStr = str(user).encode('ascii', 'ignore').decode('ascii')
            # f.write(userStr + "\n")
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

print("started...")
userList = []
finishedList = pd.read_csv("./user_profile/finishedList.csv",header=None).values.tolist() 
finishedList = [x[0] for x in finishedList]

dfUserList = pd.read_csv("Unique.csv",header=None)
userlist = dfUserList[0].values.tolist()
print("user List = ",userlist[:10])
for u in userlist:
   if u not in finishedList:
      userList.append(u)
getUserInfo(userList)
print("Done")
  
