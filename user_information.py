import tweepy
from tweepy import Stream
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
import time
from appMng import appMng
import pandas as pd
import os

fol = "./user_info/IA/"

consumer_key = "i4ReUBPhLUFNlGYfk5wBDZaAl"
consumer_secret = "YGe1TfIlBeo3DSKZ6cKzX5hD8Pkw3Pdgfv1OYKhSP2Z4fbZVyS"
access_key = "1973722680-GJon8YENN4i8FLOYxypXaMASlUfriceRZKXGj0r"
access_secret = "H5xnyIJ410E4qRjfIuS0fJYIxIbZ40aQJaRPAkh6UlPou"

CONSUMER_KEY = consumer_key
CONSUMER_SECRET = consumer_secret
ACCESS_KEY = access_key
ACCESS_SECRET = access_secret
auth = OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
api = tweepy.API(auth)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
class TweetListener(StreamListener):
    # A listener handles tweets are the received from the stream.
    #This is a basic listener that just prints received tweets to standard output

    def on_data(self, data):
        print (data)
        return True

    def on_error(self, status):
        print (status)
#search
api = tweepy.API(auth)
twitterStream = Stream(auth,TweetListener())

import os  

def getUserInfo(userList):
   fol = "user_profile/"
   finishedList = "./user_profile/finishedList.csv"
   
   fnFile = open(finishedList,"a")
   (CONSUMER_KEY,CONSUMER_SECRET,ACCESS_KEY,ACCESS_SECRET) = appMng(2)
   auth = OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
   api = tweepy.API(auth)
   auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
   userCount = len(userList)
   print("len userList: ",str(userCount))
   #test = api.lookup_users(screen_names= userList)
   
   block = 0
   blockSize = 50
   while block < userCount:
      try:
         test = api.lookup_users(screen_names= userList[block:(block+10)])
         for i,user in enumerate(test):
          with open(fol + user.screen_name  + ".csv","w") as f:

       #fuck you

            print("writing for user ",user.screen_name)
            userStr = str(user).encode('ascii', 'ignore').decode('ascii')
            f.write(userStr + "\n")
            block+=1
     
            print("block, i = ",block,i)
          fnFile.write(user.screen_name + ".csv \n")

      except Exception as e:
         print("e,block i = ",e,block,i)
         if 'Not authorized' in str(e):
             print("returning... bkup user ",user_name)
             fnFile.write(user_name + ".csv \n")
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
  
