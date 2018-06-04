import tweepy
from tweepy import Stream
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
import os
import time
import sys
import pandas as pd
from appMng import TwitterApp

consumer_key = "i4ReUBPhLUFNlGYfk5wBDZaAl"
consumer_secret = "YGe1TfIlBeo3DSKZ6cKzX5hD8Pkw3Pdgfv1OYKhSP2Z4fbZVyS"
access_key = "1973722680-GJon8YENN4i8FLOYxypXaMASlUfriceRZKXGj0r"
access_secret = "H5xnyIJ410E4qRjfIuS0fJYIxIbZ40aQJaRPAkh6UlPou"

#CONSUMER_KEY,CONSUMER_SECRET,ACCESS_KEY,ACCESS_SECRET = TwitterApp.rotateApp()
#print("key = ",CONSUMER_KEY,CONSUMER_SECRET,ACCESS_KEY,ACCESS_SECRET)

def get_followers(userList):
    CONSUMER_KEY,CONSUMER_SECRET,ACCESS_KEY,ACCESS_SECRET = TwitterApp.rotateApp()
    print("key = ",CONSUMER_KEY,CONSUMER_SECRET,ACCESS_KEY,ACCESS_SECRET)
    auth = OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
    api = tweepy.API(auth)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    
    count = 0
    totalIndex = 0
    maxUser = 200
    while totalIndex < len(userList):
       try:
          user_name = userList[totalIndex]
          print("current user = ",user_name)
          users = tweepy.Cursor(api.friends, screen_name=user_name, count=200).items()
 #        print("len users = ",len(users))
          #with open("user_followers/" + user_name + ".csv","w") as f:
          filename = "user_followings/" + user_name + ".csv"
          finishedList = "./user_followings/finishedList.csv"
          fnFile = open(finishedList,"a")
          count = 0
          for user in users:
          #   f = open(filename,append_write)
             if os.path.exists(filename):
                append_write = 'a' # append if already exists
             else:
                append_write = 'w' # make a new file if not
             f = open(filename,append_write)
             f.write(user.id_str + "," + user.screen_name + "\n")
             print("user = ",user_name,user.id_str,user.screen_name)
             count+=1
             if count >= maxUser: break 
          totalIndex+=1
          print("finished crawling.. bkup user ",user_name)
          fnFile.write(user_name + ".csv \n")
       except Exception as e:
          print("some errors...",e,e.api_code)
          if e.api_code in [130] or 'Over capacity' in str(e):
                print("over capacity...  user ",user_name)
                totalIndex+=1
          if e.api_code in [34] or 'Not authorized' in str(e) :  
                print("returning... bkup user ",user_name)
                fnFile.write(user_name + ".csv \n")
                totalIndex+=1
          else:
             print("switching account...")	  
             CONSUMER_KEY,CONSUMER_SECRET,ACCESS_KEY,ACCESS_SECRET = TwitterApp.rotateApp() 
             auth = OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
             api = tweepy.API(auth)
             auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
             time.sleep(1)
    
print("started...")
userList = []
finishedList = pd.read_csv("./user_followings/finishedList.csv",header=None).values.tolist()
#finishedList = [x[0].replace(".csv","") for x in finishedList]
fList = {}
for x in finishedList:
   fList[x[0].replace(".csv","")] = 0    
print("finished List: ",len(finishedList))


dfUserList = pd.read_csv("Unique.csv",header=None)
userlist = dfUserList[0].values.tolist()
print("user List = ",userlist[:10])

for u in userlist:
   if u not in fList:
      userList.append(u)


#for user in userList:
get_followers(userList)

print("Done")
